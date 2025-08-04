from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

role_permissions_bp = Blueprint('role_permissions', __name__)
bcrypt = Bcrypt()


@role_permissions_bp.route('/role-permissions/<uuid:role_id>', methods=['GET'])
@jwt_required
def get_role_permissions(role_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT rp.id, r.role_name, p.id AS permission_id, p.permission_name, p.description
            FROM RolePermissions rp
            JOIN Roles r ON rp.role_id = r.id
            JOIN Permissions p ON rp.permission_id = p.id
            WHERE r.id = %s
            ORDER BY r.role_name
        """, (str(role_id),))

        perms = cur.fetchall()
        result = [{"id": p[0], "role_name": p[1], "permission_name": p[3],
                   "description": p[4]} for p in perms]
        return jsonify({"role_permissions": result}), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@role_permissions_bp.route('/role-permissions', methods=['POST'])
@jwt_required
def create_role_permission():
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


@role_permissions_bp.route('/role-permissions/<uuid:role_permission_id>', methods=['PUT'])
@jwt_required
def update_role_permission(role_permission_id):
    data = request.get_json()
    role_id = data.get("role_id")
    permission_id = data.get("permission_id")

    if not role_id or not permission_id:
        return jsonify({"error": "role_id and permission_id are required"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE RolePermissions
            SET role_id = %s, permission_id = %s
            WHERE id = %s
        """, (role_id, permission_id, str(role_permission_id)))
        conn.commit()
        return jsonify({"message": "Role permission updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@role_permissions_bp.route("/role-permissions/<uuid:role_permission_id>", methods=["DELETE"])
@jwt_required
def del_role_permissions(role_permission_id):
    tenant_id = request.current_user_jwt_claims.get('tenant_id')
    if not tenant_id:
        return jsonify({"error": "tenant_id missing from JWT"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM RolePermissions WHERE id = %s",
            (str(role_permission_id),)
        )
        if cur.rowcount == 0:
            return jsonify({"error": "RolePermissions not found or tenant mismatch"}), 404
        conn.commit()
        return jsonify({"message": "RolePermissions deleted successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error deleting RolePermissions: {e}"}), 500

    finally:
        cur.close()
        conn.close()
