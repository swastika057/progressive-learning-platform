from flask import Blueprint, request, jsonify
from services.payment_service import (
    create_payment, get_payments,
    update_payment, delete_payment
)
from utils.decorators import jwt_required

payments_bp = Blueprint('payments', __name__)


@payments_bp.route('/payments', methods=['POST'])
@jwt_required
def add_payment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing payment data"}), 400

    try:
        payment = create_payment(data)
        return jsonify(payment), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@payments_bp.route('/payments/<tenant_id>/<bill_id>', methods=['GET'])
@jwt_required
def fetch_payments(tenant_id, bill_id):

    try:
        payments = get_payments(tenant_id, bill_id)
        return jsonify(payments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@payments_bp.route('/payments/<payment_id>', methods=['PUT'])
@jwt_required
def modify_payment(payment_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing payment data"}), 400

    updated = update_payment(payment_id, data)
    if not updated:
        return jsonify({"error": "Payment not found"}), 404

    return jsonify(updated), 200


@payments_bp.route('/payments/<payment_id>', methods=['DELETE'])
@jwt_required
def remove_payment(payment_id):
    result = delete_payment(payment_id)
    if result == 0:
        return jsonify({"error": "Payment not found"}), 404
    return jsonify({"message": "Payment deleted successfully"}), 200
