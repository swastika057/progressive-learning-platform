from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.enrollment_service import (
    add_enrollment_record,
    get_all_enrollments,
    update_enrollment_record,
    delete_enrollment_record
)

enrollment_bp = Blueprint('enrollment', __name__)


@enrollment_bp.route('/enrollment', methods=['POST'])
@jwt_required
def add_enrollment():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    result, error, status = add_enrollment_record(data, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@enrollment_bp.route('/enrollment', methods=['GET'])
@jwt_required
def get_enrollments():
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    result, error = get_all_enrollments(tenant_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(result), 200


@enrollment_bp.route('/enrollment/<uuid:enrollment_id>', methods=['PUT'])
@jwt_required
def update_enrollment(enrollment_id):
    data = request.get_json()
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    result, error, status = update_enrollment_record(
        enrollment_id, tenant_id, data)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@enrollment_bp.route('/enrollment/<uuid:enrollment_id>', methods=['DELETE'])
@jwt_required
def delete_enrollment(enrollment_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    result, error, status = delete_enrollment_record(enrollment_id, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status
