from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.permissions_service import (
    get_all_permissions,
    create_permission,
    update_permission_by_id,
    delete_permission_by_id
)

permissions_bp = Blueprint('permissions', __name__)


@permissions_bp.route('/permissions', methods=['GET'])
@jwt_required
# @admin_required
def get_permissions():
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    result, error = get_all_permissions(tenant_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(permissions=result), 200


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

    success, error = create_permission(permission_name, description, tenant_id)
    if not success:
        return jsonify({"error": error}), 500
    return jsonify({"message": "Permission added successfully"}), 201


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

    success, error, not_found = update_permission_by_id(
        permission_id, permission_name, description, tenant_id)
    if not success:
        if not_found:
            return jsonify({"error": "Permission not found"}), 404
        return jsonify({"error": error}), 500

    return jsonify({"message": "Permission updated successfully"}), 200


@permissions_bp.route('/permissions/<uuid:permission_id>', methods=['DELETE'])
@jwt_required
# @admin_required
def delete_permission(permission_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    success, error, not_found = delete_permission_by_id(
        permission_id, tenant_id)
    if not success:
        if not_found:
            return jsonify({"error": "Permission not found"}), 404
        return jsonify({"error": error}), 500

    return jsonify({"message": "Permission deleted successfully"}), 200
