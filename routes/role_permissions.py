
from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

roles_permission = Blueprint('Roles_Permission', __name__)

bcrypt = Bcrypt()


@roles_permission.route('/role_permissions/<uuid:role_id>', methods=['GET'])
@jwt_required
def get_permissions_for_role(role_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT  rp.id,
                    r.role_name,
                    p.id AS permission_id,
                    p.permission_name,
                    p.description
                FROM RolePermissions rp
                JOIN Roles r ON rp.role_id = r.id
                JOIN Permissions p ON rp.permission_id = p.id
                ORDER BY r.role_name

        """, (str(role_id),))
        perms = cur.fetchall()
        result = [{"id": p[0], "role_name": p[1], "permission_name": p[3],
                   "description": p[4]} for p in perms]
        return jsonify(role_permissions=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@roles_permission.route('/role_permissions/add', methods=['POST'])
@jwt_required
# @admin_required
def add_role_permission():
    data = request.get_json()
    role_id = data.get("role_id")
    permission_id = data.get("permission_id")

    if not role_id or not permission_id:
        return jsonify({"error": "role_id and permission_id are required"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO RolePermissions (role_id, permission_id)
            VALUES (%s, %s)
            ON CONFLICT (role_id, permission_id) DO NOTHING
        """, (role_id, permission_id))
        conn.commit()
        return jsonify({"message": "Permission assigned to role"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
