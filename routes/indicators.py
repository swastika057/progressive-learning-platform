from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.indicators_service import (
    create_indicator,
    get_indicators,
    update_indicator,
    delete_indicator,
)

indicators_bp = Blueprint("indicators", __name__)


@indicators_bp.route('/indicators', methods=['POST'])
@jwt_required
def create_indicator_route():
    data = request.get_json()
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    result, error, status = create_indicator(data, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@indicators_bp.route('/indicators', methods=['GET'])
@jwt_required
def get_indicators_route():
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    result, error = get_indicators(tenant_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(result), 200


@indicators_bp.route('/indicators/<uuid:indicator_id>', methods=['PUT'])
@jwt_required
def update_indicator_route(indicator_id):
    data = request.get_json()
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    result, error, status = update_indicator(indicator_id, tenant_id, data)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@indicators_bp.route('/indicators/<uuid:indicator_id>', methods=['DELETE'])
@jwt_required
def delete_indicator_route(indicator_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    result, error, status = delete_indicator(indicator_id, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status
