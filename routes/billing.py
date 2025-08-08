from flask import Blueprint, request, jsonify
from services.billing_service import create_billing, get_all_billing, update_billing, delete_billing
from utils.decorators import jwt_required

billing_bp = Blueprint('billing', __name__)


@billing_bp.route('/billing', methods=['POST'])
@jwt_required
def create_bill():
    data = request.get_json()
    return create_billing(data)


@billing_bp.route('/billing', methods=['GET'])
@jwt_required
def get_bills():
    return get_all_billing()


@billing_bp.route('/billing/<uuid:billing_id>', methods=['PUT'])
@jwt_required
def update_bill(billing_id):
    data = request.get_json()
    return update_billing(billing_id, data)


@billing_bp.route('/billing/<uuid:billing_id>', methods=['DELETE'])
@jwt_required
def delete_bill(billing_id):
    return delete_billing(billing_id)
