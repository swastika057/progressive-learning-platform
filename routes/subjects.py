from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.subjects_service import (
    add_subject,
    get_subjects,
    update_subject,
    delete_subject,
)

subjects_bp = Blueprint('subjects', __name__)


@subjects_bp.route('/subjects', methods=['POST'])
@jwt_required
def add_subject_route():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    result, error, status = add_subject(data, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@subjects_bp.route('/subjects', methods=['GET'])
@jwt_required
def get_subjects_route():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    result, error = get_subjects(tenant_id)
    if error:
        return jsonify({"error": error}), 500
    return jsonify(subjects=result), 200


@subjects_bp.route('/subjects/<uuid:id>', methods=['PUT'])
@jwt_required
def update_subject_route(id):
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    result, error, status = update_subject(id, tenant_id, data)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status


@subjects_bp.route('/subjects/<uuid:id>', methods=['DELETE'])
@jwt_required
def delete_subject_route(id):
    tenant_id = request.current_user_jwt_claims.get('tenant_id')
    result, error, status = delete_subject(id, tenant_id)
    if error:
        return jsonify({"error": error}), status
    return jsonify({"message": result}), status
