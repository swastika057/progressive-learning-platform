# routes/billtypes.py

from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.billtype_service import (
    add_bill_type_service,
    get_bill_types_service,
    update_bill_type_service,
    delete_bill_type_service
)

billtypes_bp = Blueprint("bill_type", __name__)


@billtypes_bp.route('/billtypes', methods=['POST'])
@jwt_required
def add_bill_type():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    bill_type_name = data.get('bill_type_name')
    description = data.get('description')

    response, status = add_bill_type_service(
        tenant_id, bill_type_name, description)
    return jsonify(response), status


@billtypes_bp.route('/billtypes', methods=['GET'])
@jwt_required
def get_bill_types():
    tenant_id = request.current_user_jwt_claims.get('tenant_id')
    if not tenant_id:
        return jsonify({"error": "Tenant ID missing in token"}), 400
    response, status = get_bill_types_service(tenant_id)
    return jsonify(response), status


@billtypes_bp.route('/billtypes/<uuid:bill_type_id>', methods=['PUT'])
@jwt_required
def update_bill_type(bill_type_id):
    data = request.get_json()
    bill_type_name = data.get('bill_type_name')
    description = data.get('description')

    response, status = update_bill_type_service(
        bill_type_id, bill_type_name, description)
    return jsonify(response), status


@billtypes_bp.route('/billtypes/<uuid:bill_type_id>', methods=['DELETE'])
@jwt_required
def delete_bill_type(bill_type_id):
    response, status = delete_bill_type_service(bill_type_id)
    return jsonify(response), status
