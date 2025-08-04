from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

user_roles_bp = Blueprint('user_roles', __name__)


@user_roles_bp.route('/user-roles', methods=['POST'])
@jwt_required
# @admin_required
def add_user_role():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    user_id = data.get('user_id')
    role_id = data.get('role_id')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    if not all([user_id, role_id, tenant_id]):
        return jsonify({"error": "user_id, role_id, and tenant_id are required."}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO UserRoles (user_id, role_id, tenant_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, role_id, tenant_id) DO NOTHING
        """, (user_id, role_id, tenant_id))
        conn.commit()
        return jsonify({"message": "User role assigned successfully!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@user_roles_bp.route('/user-roles', methods=['GET'])
@jwt_required
# @admin_required
def get_user_roles():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                ur.id,
                u.username,
                r.role_name,
                t.tenant_name
            FROM UserRoles ur
            JOIN Users u ON ur.user_id = u.id
            JOIN Roles r ON ur.role_id = r.id
            JOIN Tenants t ON ur.tenant_id = t.id
        """)
        rows = cur.fetchall()
        result = []
        for row in rows:
            result.append({
                "id": row[0],
                "username": row[1],
                "role_name": row[2],
                "tenant_name": row[3]
            })
        return jsonify(user_roles=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@user_roles_bp.route('/user-roles/<uuid:id>', methods=['PUT'])
@jwt_required
# @admin_required
def user_roles_update(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    user_id = data.get('user_id')
    role_id = data.get('role_id')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    if not all([user_id, role_id, tenant_id]):
        return jsonify({"error": "user_id, role_id, and tenant_id are required."}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE UserRoles 
            SET user_id = %s, role_id = %s, tenant_id = %s
            WHERE id = %s
        """, (user_id, role_id, tenant_id, str(id)))
        conn.commit()
        return jsonify({"message": "User role updated successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@user_roles_bp.route('/user-roles/<uuid:id>', methods=['DELETE'])
@jwt_required
# @admin_required
def user_roles_delete(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM UserRoles WHERE id = %s", (str(id),))
        conn.commit()
        return jsonify({"message": "User role deleted successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
