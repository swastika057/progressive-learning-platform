from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

permissions_bp = Blueprint('permissions', __name__)


@permissions_bp.route('/permissions', methods=['GET'])
@jwt_required
# @admin_required
def get_permissions():
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, permission_name, description 
            FROM Permissions
            WHERE tenant_id = %s
        """, (tenant_id,))

        permissions = cur.fetchall()
        result = [{"id": p[0], "permission_name": p[1],
                   "description": p[2]} for p in permissions]
        return jsonify(permissions=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@permissions_bp.route('/permissions', methods=['POST'])
@jwt_required
# @admin_required
def add_permission():
    data = request.get_json()
    permission_name = data.get("permission_name")
    description = data.get("description")
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")

    if not permission_name or not tenant_id:
        return jsonify({"error": "permission_name and tenant_id are required"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Permissions (permission_name, description, tenant_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (permission_name, tenant_id) DO NOTHING
        """, (permission_name, description, tenant_id))
        conn.commit()
        return jsonify({"message": "Permission added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@permissions_bp.route('/permissions/<uuid:permission_id>', methods=['PUT'])
@jwt_required
# @admin_required
def update_permission(permission_id):
    data = request.get_json()
    permission_name = data.get("permission_name")
    description = data.get("description")
    tenant_id = request.current_user_jwt_claims.get("tenant_id")

    if not permission_name or not tenant_id:
        return jsonify({"error": "permission_name is required"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Permissions
            SET permission_name = %s,
                description = %s
            WHERE id = %s AND tenant_id = %s
        """, (permission_name, description, str(permission_id), tenant_id))

        if cur.rowcount == 0:
            return jsonify({"error": "Permission not found"}), 404

        conn.commit()
        return jsonify({"message": "Permission updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@permissions_bp.route('/permissions/<uuid:permission_id>', methods=['DELETE'])
@jwt_required
# @admin_required
def delete_permission(permission_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Permissions
            WHERE id = %s AND tenant_id = %s
        """, (str(permission_id), tenant_id))

        if cur.rowcount == 0:
            return jsonify({"error": "Permission not found"}), 404

        conn.commit()
        return jsonify({"message": "Permission deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
