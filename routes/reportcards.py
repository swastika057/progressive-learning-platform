from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.reportcards_service import (
    add_report_card_service,
    get_all_report_cards_service,
    get_report_card_service,
    update_report_card_service,
    delete_report_card_service
)

report_card_bp = Blueprint('report_cards', __name__)


@report_card_bp.route('/report-cards', methods=['POST'])
@jwt_required
def add_report_card():
    data = request.get_json()
    required_fields = ['tenant_id', 'student_id',
                       'academic_year_id', 'semester']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400
    response, status = add_report_card_service(data)
    return jsonify(response), status


@report_card_bp.route('/report-cards', methods=['GET'])
@jwt_required
def get_all_report_cards():
    response, status = get_all_report_cards_service()
    return jsonify(response), status


@report_card_bp.route('/report-cards/<uuid:report_card_id>', methods=['GET'])
@jwt_required
def get_report_card(report_card_id):
    response, status = get_report_card_service(str(report_card_id))
    return jsonify(response), status


@report_card_bp.route('/report-cards/<uuid:report_card_id>', methods=['PUT'])
@jwt_required
def update_report_card(report_card_id):
    data = request.get_json()
    response, status = update_report_card_service(str(report_card_id), data)
    return jsonify(response), status


@report_card_bp.route('/report-cards/<uuid:report_card_id>', methods=['DELETE'])
@jwt_required
def delete_report_card(report_card_id):
    response, status = delete_report_card_service(str(report_card_id))
    return jsonify(response), status
