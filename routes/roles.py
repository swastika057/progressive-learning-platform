from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.roles_services import (
    fetch_roles, create_role, update_role_by_id, delete_role_by_id)


roles_bp = Blueprint('roles', __name__)


@roles_bp.route('/roles', methods=['GET'])
@jwt_required
def get_roles():

    roles_data, error = fetch_roles()
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"roles": roles_data}), 200


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

    message, error = create_role(role_name, description, tenant_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"message": message}), 201


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

    message, error = update_role_by_id(
        role_id, role_name, description, tenant_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"message": message}), 200


@roles_bp.route('/roles/<uuid:role_id>', methods=['DELETE'])
@jwt_required
# @admin_required
def del_role(role_id):
    message, error = delete_role_by_id(role_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"message": message}), 200
