from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.indicator_items_service import (
    create_indicator_item,
    update_indicator_item,
    delete_indicator_item,
    list_indicator_items,
)

indicator_items_bp = Blueprint("indicator_items", __name__)


@indicator_items_bp.route("/indicator-items", methods=["POST"])
@jwt_required
def create_indicator_item_route():
    data = request.get_json()
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    result, error, status = create_indicator_item(data, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@indicator_items_bp.route("/indicator-items/<uuid:item_id>", methods=["PUT"])
@jwt_required
def update_indicator_item_route(item_id):
    data = request.get_json()
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    result, error, status = update_indicator_item(item_id, tenant_id, data)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@indicator_items_bp.route("/indicator-items/<uuid:item_id>", methods=["DELETE"])
@jwt_required
def delete_indicator_item_route(item_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    result, error, status = delete_indicator_item(item_id, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@indicator_items_bp.route("/indicator-items", methods=["GET"])
@jwt_required
def list_indicator_items_route():
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    result, error = list_indicator_items(tenant_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(result), 200
