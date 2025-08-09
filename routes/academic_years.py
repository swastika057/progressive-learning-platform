from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.academicyear_service import (
    get_all_academic_years,
    create_academic_year,
    update_academic_year,
    delete_academic_year
)

academic_years = Blueprint('Academic_years', __name__)


@academic_years.route('/academic-years', methods=['GET'])
@jwt_required
def get_academic_years():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get("tenant_id")
    try:
        result = get_all_academic_years(tenant_id)
        return jsonify(years=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@academic_years.route('/academic-years', methods=['POST'])
@jwt_required
def add_academic_years():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    year_label = data.get('year_label')

    if not tenant_id or not year_label:
        return jsonify({"error": "tenant_id and year_label are required"}), 400

    try:
        create_academic_year(tenant_id, year_label)
        return jsonify({"message": "AcademicYear created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@academic_years.route('/academic-years/<int:year_id>', methods=['PUT'])
@jwt_required
def update_academic_year_route(year_id):
    data = request.get_json()
    year_label = data.get('year_label')

    if not year_label:
        return jsonify({"error": "year_label is required"}), 400

    try:
        updated = update_academic_year(year_id, year_label)
        if not updated:
            return jsonify({"error": "AcademicYear not found"}), 404
        return jsonify({"message": "AcademicYear updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@academic_years.route('/academic-years/<int:year_id>', methods=['DELETE'])
@jwt_required
def delete_academic_year_route(year_id):
    try:
        deleted = delete_academic_year(year_id)
        if not deleted:
            return jsonify({"error": "AcademicYear not found"}), 404
        return jsonify({"message": "AcademicYear deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
