# routes/milestones.py

from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.milestone_service import (
    create_milestone_service,
    get_milestones_service,
    update_milestone_service,
    delete_milestone_service
)

milestones_bp = Blueprint("milestones", __name__)


@milestones_bp.route("/milestones", methods=["POST"])
@jwt_required
def create_milestone():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    milestone = data.get("milestone")
    description = data.get("description")

    response, status = create_milestone_service(
        tenant_id, milestone, description)
    return jsonify(response), status


@milestones_bp.route("/milestones", methods=["GET"])
@jwt_required
def get_milestones():
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    response, status = get_milestones_service(tenant_id)
    return jsonify(response), status


@milestones_bp.route("/milestones/<milestone_id>", methods=["PUT"])
@jwt_required
def update_milestone(milestone_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    description = data.get("description")

    response, status = update_milestone_service(
        milestone_id, tenant_id, description)
    return jsonify(response), status


@milestones_bp.route("/milestones/<milestone_id>", methods=["DELETE"])
@jwt_required
def delete_milestone(milestone_id):
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    response, status = delete_milestone_service(milestone_id, tenant_id)
    return jsonify(response), status
