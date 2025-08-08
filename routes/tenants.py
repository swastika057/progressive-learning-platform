from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.tenant_services import get_all_tenants, update_tenant_by_id, delete_tenant_by_id

tenant_bp = Blueprint('tenants', __name__)


@tenant_bp.route('/tenants', methods=['GET'])
@jwt_required
def get_tenants():
    user_claims = request.current_user_jwt_claims
    tenants_list, error = get_all_tenants(user_claims)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(tenants=tenants_list), 200


@tenant_bp.route('/tenants/<uuid:id>', methods=['PUT'])
@jwt_required
# @admin_required
def update_tenant(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    message, error = update_tenant_by_id(id, data)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"message": message}), 200


@tenant_bp.route("/tenants/<uuid:id>", methods=["DELETE"])
@jwt_required
# @admin_required
def delete_tenant(id):
    message, error = delete_tenant_by_id(id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify({"message": message}), 200
