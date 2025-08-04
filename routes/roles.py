from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

roles_bp = Blueprint('roles', __name__)


@roles_bp.route('/roles', methods=['GET'])
@jwt_required
def get_roles():
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT id,role_name ,tenant_id,description from roles """)
        roles_data = cur.fetchall()
        roles_list = []
        for role in roles_data:
            roles_list.append({
                "id": role[0],
                "roles_name": role[1],
                "tenant_id": role[2],
                "description": role[3]
            })
        return jsonify(roles=roles_list), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@roles_bp.route('/roles', methods=['POST'])
@jwt_required
# @admin_required
def add_roles():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid json"}), 400
    role_name = data.get('role_name')
    description = data.get('description')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    if not role_name or not tenant_id:
        return jsonify({"error": "Role name and tenant_id are required."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO Roles(role_name,description,tenant_id)VALUES(%s,%s,%s)""", (
            role_name,  description, tenant_id))
        conn.commit()
        return jsonify({"message": "Roles added successfully!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str({e})}), 500
    finally:
        cur.close()
        conn.close()


@roles_bp.route('/roles/<uuid:role_id>', methods=['PUT'])
@jwt_required
# @admin_required
def update_role(role_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    role_name = data.get("role_name")
    description = data.get("description")
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get('tenant_id')

    if not role_name or not tenant_id:
        return jsonify({"error": "Role name and tenant_id are required."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed!"}), 500

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Roles SET
            role_name = %s,
            description = %s
            WHERE tenant_id = %s AND id = %s
        """, (role_name, description, str(tenant_id), str(role_id)))
        conn.commit()
        return jsonify({"message": "Role updated successfully!"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@roles_bp.route('/roles/<uuid:role_id>', methods=['DELETE'])
@jwt_required
# @admin_required
def del_role(role_id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM roles where id=%s", (str(role_id),))
        conn.commit()
        return jsonify({"message": "Role deleted successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
