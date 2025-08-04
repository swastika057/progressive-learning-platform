from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone
from psycopg2.extras import RealDictCursor

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
@jwt_required
# @admin_required
def get_users():
    user_claims = request.current_user_jwt_claims
    is_admin = user_claims.get('is_admin')
    tenant_id = user_claims.get('tenant_id')
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        if is_admin and not tenant_id:
            cur.execute("""
                SELECT * FROM Users
            """)
        else:
            if not tenant_id:
                return jsonify({"error": "Missing tenant_id in JWT claims"}), 400
            cur.execute("""
                SELECT id, username, email, first_name, last_name, contact_phone, tenant_id,
                gender, date_of_birth, is_active, last_login, created_at, updated_at
                FROM Users

                
        """, (str(tenant_id),))
        users = cur.fetchall()
        user_list = []
        for user in users:
            user_list.append({
                "id": str(user["id"]),
                "username": user["username"],
                "email": user["email"],
                "first_name": user["first_name"],
                "last_name": user["last_name"],
                "contact_phone": user["contact_phone"],
                "gender": user["gender"],
                "tenant_id": user["tenant_id"],
                "date_of_birth": user["date_of_birth"].isoformat() if user["date_of_birth"] else None,
                "is_active": user["is_active"],
                "last_login": user["last_login"].isoformat() if user["last_login"] else None,
                "created_at": user["created_at"].isoformat() if user["created_at"] else None,
                "updated_at": user["updated_at"].isoformat() if user["updated_at"] else None

            })
        return jsonify(users=user_list), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@users_bp.route("/users", methods=["POST"])
@jwt_required
# @admin_required
def add_user():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    username = data.get('username')
    password = data.get('password')  # not hashed yet
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_phone = data.get('contact_phone')
    gender = data.get('gender')
    date_of_birth = data.get('date_of_birth')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    if not username or not password or not email or not tenant_id:
        return jsonify({"error": "Username, password, email, and tenant_id are required."}), 400

    try:
        dob_obj = datetime.strptime(
            date_of_birth, "%Y-%m-%d").date() if date_of_birth else None
    except ValueError:
        return jsonify({"error": "Invalid date_of_birth. Use YYYY-MM-DD."}), 400

    password_hash = bcrypt.generate_password_hash(
        password).decode('utf-8')

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Users (username, password_hash, email, first_name, last_name,
                               contact_phone, gender, date_of_birth, tenant_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
        """, (username, password_hash, email, first_name, last_name,
              contact_phone, gender, dob_obj, tenant_id))
        conn.commit()
        return jsonify({"message": "User added successfully"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@users_bp.route("/users/<uuid:user_id>", methods=["PUT"])
@jwt_required
# @admin_required
def update_user(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_phone = data.get('contact_phone')
    gender = data.get('gender')
    date_of_birth = data.get('date_of_birth')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    if not username or not password or not email or not tenant_id:
        return jsonify({"error": "Username, password, email, and tenant_id are required."}), 400

    try:
        dob_obj = datetime.strptime(
            date_of_birth, "%Y-%m-%d").date() if date_of_birth else None
    except ValueError:
        return jsonify({"error": "Invalid date_of_birth. Use YYYY-MM-DD."}), 400

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection(cursor_factory=RealDictCursor)
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Users SET
                username = %s,
                password_hash = %s,
                email = %s,
                first_name = %s,
                last_name = %s,
                contact_phone = %s,
                gender = %s,
                date_of_birth = %s,
                tenant_id = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
        """, (
            username, password_hash, email, first_name, last_name,
            contact_phone, gender, dob_obj, tenant_id, str(user_id)
        ))
        conn.commit()
        return jsonify({"message": "User updated successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@users_bp.route("/users/<uuid:user_id>", methods=["DELETE"])
@jwt_required
# @admin_required
def del_users(user_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the datbase"}), 500
    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        cur.execute("DELETE FROM Users where id=%s", (str(user_id),))
        cur.commit()
        return jsonify({"message": "User deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
