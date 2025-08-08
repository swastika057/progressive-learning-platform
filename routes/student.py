from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.student_service import (
    add_student,
    get_students,
    update_student,
    delete_student
)

students_bp = Blueprint('student', __name__)


@students_bp.route('/students', methods=['POST'])
@jwt_required
def add_student_route():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    user_id = data.get('user_id')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    roll_no = data.get('roll_no')
    dob = data.get('date_of_birth')
    address = data.get('address')
    parent_name = data.get('parent_name')
    parent_contact = data.get('parent_contact')
    enrollment_date = data.get('enrollment_date')

    if not user_id or not tenant_id or not roll_no:
        return jsonify({"error": "user_id, tenant_id, and roll_no are required."}), 400

    try:
        add_student(user_id, tenant_id, roll_no, dob, address,
                    parent_name, parent_contact, enrollment_date)
        return jsonify({"message": "Student added successfully!"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@students_bp.route('/students', methods=['GET'])
@jwt_required
def get_students_route():
    try:
        students = get_students()
        return jsonify(students=students), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@students_bp.route('/students/<uuid:user_id>', methods=['PUT'])
@jwt_required
def update_student_route(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    roll_no = data.get('roll_no')
    dob = data.get('date_of_birth')
    address = data.get('address')
    parent_name = data.get('parent_name')
    parent_contact = data.get('parent_contact')
    enrollment_date = data.get('enrollment_date')

    if not tenant_id:
        return jsonify({"error": "tenant_id is required."}), 400

    try:
        updated = update_student(user_id, tenant_id, roll_no, dob,
                                 address, parent_name, parent_contact, enrollment_date)
        if updated == 0:
            return jsonify({"error": "Student not found or tenant mismatch"}), 404
        return jsonify({"message": "Student updated successfully!"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@students_bp.route("/students/<uuid:user_id>", methods=["DELETE"])
@jwt_required
def delete_student_route(user_id):
    tenant_id = request.current_user_jwt_claims.get('tenant_id')
    if not tenant_id:
        return jsonify({"error": "tenant_id missing from JWT"}), 400

    try:
        deleted = delete_student(user_id, tenant_id)
        if deleted == 0:
            return jsonify({"error": "Student not found or tenant mismatch"}), 404
        return jsonify({"message": "Student deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": f"Error deleting student: {e}"}), 500
