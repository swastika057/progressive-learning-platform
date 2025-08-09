# routes/remarks.py

from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.remarks_service import (
    add_remark_service,
    get_remarks_service,
    update_remark_service,
    delete_remark_service,
)

remarks_bp = Blueprint("remarks", __name__)

# CREATE


@remarks_bp.route('/remarks', methods=['POST'])
@jwt_required
def add_remark():
    data = request.get_json()
    data['tenant_id'] = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    recorded_by = request.current_user_jwt_claims.get('user_id')
    response, status = add_remark_service(data, recorded_by)
    return jsonify(response), status


# READ
@remarks_bp.route('/remarks', methods=['GET'])
@jwt_required
def get_remarks():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    response, status = get_remarks_service(tenant_id)
    return jsonify(response), status


# UPDATE
@remarks_bp.route('/remarks/<uuid:remark_id>', methods=['PUT'])
@jwt_required
def update_remark(remark_id):
    data = request.get_json()
    comment = data.get('comment')
    semester = data.get('semester')
    response, status = update_remark_service(remark_id, comment, semester)
    return jsonify(response), status


# DELETE
@remarks_bp.route('/remarks/<uuid:remark_id>', methods=['DELETE'])
@jwt_required
def delete_remark(remark_id):
    response, status = delete_remark_service(remark_id)
    return jsonify(response), status
