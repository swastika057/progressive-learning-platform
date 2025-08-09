# routes/class_subject_routes.py

from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.class_sub_service import (
    add_class_subject_logic,
    get_all_class_subjects_logic,
    update_class_subject_logic,
    delete_class_subject_logic
)

class_sub = Blueprint('class-subject', __name__)


@class_sub.route('/class-subjects', methods=['POST'])
@jwt_required
def add_class_subject():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    result, status = add_class_subject_logic(data, tenant_id)
    return jsonify(result), status


@class_sub.route('/class-subjects', methods=['GET'])
@jwt_required
def class_subject():
    result, status = get_all_class_subjects_logic()
    return jsonify(class_subject=result), status


@class_sub.route('/class-subjects/<uuid:class_subject_id>', methods=['PUT'])
@jwt_required
def update_class_subject(class_subject_id):
    data = request.get_json()
    result, status = update_class_subject_logic(class_subject_id, data)
    return jsonify(result), status


@class_sub.route('/class-subjects/<uuid:class_subject_id>', methods=['DELETE'])
@jwt_required
def delete_class_subject(class_subject_id):
    result, status = delete_class_subject_logic(class_subject_id)
    return jsonify(result), status
