from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.jwt_handler import create_jwt_token
from psycopg2.extras import RealDictCursor

login = Blueprint('login', __name__)

# replace with your superadmin email
SUPERADMIN_EMAIL = 'superadmin@example.com'


@login.route('/users/login', methods=['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    if not email or not password:
        return jsonify({"msg": "Email and password are required"}), 400

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)

    try:
        # Find user by email and active status
        cur.execute("""
            SELECT id, username, email, password_hash, tenant_id
            FROM Users WHERE email = %s AND is_active = TRUE
        """, (email,))
        user = cur.fetchone()

        if not user:
            return jsonify({"msg": "Invalid email or password"}), 401

        # Verify password
        if not bcrypt.check_password_hash(user['password_hash'], password):
            return jsonify({"msg": "Invalid email or password"}), 401

        # Fetch roles assigned to user for that tenant
        cur.execute("""
            SELECT R.role_name FROM UserRoles UR
            JOIN Roles R ON UR.role_id = R.id
            WHERE UR.user_id = %s AND UR.tenant_id = %s
        """, (user['id'], user['tenant_id']))
        roles = [row['role_name'] for row in cur.fetchall()]

        # If no roles and superadmin email, assign superadmin role dynamically
        if not roles and email.lower() == SUPERADMIN_EMAIL:
            roles = ['superadmin']

        token = create_jwt_token(
            user_id=str(user['id']),
            username=user['username'],
            email=user['email'],
            tenant_id=str(user['tenant_id']),
            roles=roles,
            # is_admin=user['is_admin']
        )

        return jsonify(access_token=token), 200

    except Exception as e:
        return jsonify({"msg": f"Login failed: {str(e)}"}), 500

    finally:
        cur.close()
        conn.close()
