from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.decorators import jwt_required
from services.user_role_services import (
    create_user_role,
    get_all_user_roles,
    update_user_role,
    delete_user_role
)

user_roles_bp = Blueprint('user_roles', __name__)

# CREATE


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

    success, error = create_user_role(user_id, role_id, tenant_id)
    if not success:
        return jsonify({"error": error}), 500

    return jsonify({"message": "User role assigned successfully!"}), 201


# READ
@user_roles_bp.route('/user-roles', methods=['GET'])
@jwt_required
# @admin_required
def get_user_roles():
    result, error = get_all_user_roles()
    if error:
        return jsonify({"error": error}), 500
    return jsonify(user_roles=result), 200


# UPDATE
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

    success, error = update_user_role(id, user_id, role_id, tenant_id)
    if not success:
        return jsonify({"error": error}), 500

    return jsonify({"message": "User role updated successfully!"}), 200


# DELETE
@user_roles_bp.route('/user-roles/<uuid:id>', methods=['DELETE'])
@jwt_required
# @admin_required
def user_roles_delete(id):
    success, error = delete_user_role(id)
    if not success:
        return jsonify({"error": error}), 500
    return jsonify({"message": "User role deleted successfully!"}), 200
