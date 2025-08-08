# routes/employees.py
from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.employee_service import (
    get_all_employees,
    create_employee,
    update_employee,
    delete_employee
)

employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/employees', methods=['GET'])
@jwt_required
def get_employee():
    try:
        employees = get_all_employees()
        return jsonify(employees=employees), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employees_bp.route('/employees', methods=['POST'])
@jwt_required
def create_employee_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    user_id = data.get("user_id")
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    department = data.get("department")
    hire_date = data.get("hire_date")
    qualifications = data.get("qualifications")

    if not user_id or not tenant_id:
        return jsonify({"error": "user_id and tenant_id are required!"}), 400

    try:
        create_employee(user_id, tenant_id, department,
                        hire_date, qualifications)
        return jsonify({"message": "Employee added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employees_bp.route('/employees/<uuid:id>', methods=['PUT'])
@jwt_required
def update_employee_route(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    user_id = data.get("user_id")
    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    department = data.get("department")
    hire_date = data.get("hire_date")
    qualifications = data.get("qualifications")

    if not user_id or not tenant_id:
        return jsonify({"error": "user_id and tenant_id are required!"}), 400

    try:
        update_employee(id, user_id, tenant_id, department,
                        hire_date, qualifications)
        return jsonify({"message": "Employee updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@employees_bp.route('/employees/<uuid:id>', methods=['DELETE'])
@jwt_required
def delete_employee_route(id):
    try:
        deleted = delete_employee(id)
        if deleted == 0:
            return jsonify({"error": "Employee not found"}), 404
        return jsonify({"message": "Employee deleted successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
