from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt

from utils.jwt_handler import create_jwt_token
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta, timezone


login = Blueprint('login', __name__)


@login.route('/users/login', methods=['POST'])
def user_login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')

    conn = get_db_connection(cursor_factory=RealDictCursor)
    cur = conn.cursor()

    try:
        cur.execute("""
            SELECT id, username,email, password_hash, tenant_id, is_admin
            FROM Users WHERE username = %s AND is_active = TRUE    """, (username,))
        user = cur.fetchone()

        if user and bcrypt.check_password_hash(user['password_hash'], password):
            cur.execute("""
                SELECT R.role_name FROM UserRoles UR
                JOIN Roles R ON UR.role_id = R.id
                WHERE UR.user_id = %s
            """, (user['id'],))
            roles = [row[0] for row in cur.fetchall()]

            token = create_jwt_token(
                user_id=str(user['id']),
                username=user['username'],
                email=user['email'],
                tenant_id=str(user['tenant_id']),
                roles=roles,
                is_admin=user['is_admin']
            )

            return jsonify(access_token=token), 200
        else:
            return jsonify({"msg": "Invalid username or password"}), 401

    except Exception as e:
        return jsonify({"msg": f"Login failed: {e}"}), 500

    finally:
        cur.close()
        conn.close()
