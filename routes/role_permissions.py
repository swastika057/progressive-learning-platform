from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.role_permissions_service import (
    get_permissions_for_role,
    assign_permission_to_role,
    update_role_permission,
    delete_role_permission_by_id
)

role_permissions_bp = Blueprint('role_permissions', __name__)


@role_permissions_bp.route('/role-permissions/<uuid:role_id>', methods=['GET'])
@jwt_required
def get_role_permissions(role_id):
    result, error = get_permissions_for_role(role_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"role_permissions": result}), 200


@role_permissions_bp.route('/role-permissions', methods=['POST'])
@jwt_required
def create_role_permission():
    data = request.get_json()
    role_id = data.get("role_id")
    permission_id = data.get("permission_id")

    if not role_id or not permission_id:
        return jsonify({"error": "role_id and permission_id are required"}), 400

    success, error = assign_permission_to_role(role_id, permission_id)
    if not success:
        return jsonify({"error": error}), 500
    return jsonify({"message": "Permission assigned to role"}), 201


@role_permissions_bp.route('/role-permissions/<uuid:role_permission_id>', methods=['PUT'])
@jwt_required
def update_role_permission_route(role_permission_id):
    data = request.get_json()
    role_id = data.get("role_id")
    permission_id = data.get("permission_id")

    if not role_id or not permission_id:
        return jsonify({"error": "role_id and permission_id are required"}), 400

    success, error = update_role_permission(
        role_permission_id, role_id, permission_id)
    if not success:
        return jsonify({"error": error}), 500
    return jsonify({"message": "Role permission updated successfully"}), 200


@role_permissions_bp.route("/role-permissions/<uuid:role_permission_id>", methods=["DELETE"])
@jwt_required
def del_role_permissions(role_permission_id):
    success, error, not_found = delete_role_permission_by_id(
        role_permission_id)
    if not success:
        if not_found:
            return jsonify({"error": "RolePermissions not found"}), 404
        return jsonify({"error": error}), 500
    return jsonify({"message": "RolePermissions deleted successfully"}), 200
