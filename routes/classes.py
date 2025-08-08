from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.class_service import add_class, get_classes_by_tenant, update_class, delete_class

classes_bp = Blueprint('classes', __name__)


@classes_bp.route('/classes', methods=['POST'])
@jwt_required
def add_class_route():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    academic_year_id = data.get('academic_year_id')
    class_name = data.get('class_name')
    section = data.get('section')
    teacher_id = data.get('teacher_id')

    if not all([tenant_id, academic_year_id, class_name]):
        return jsonify({"error": "Missing required fields: tenant_id, academic_year_id, class_name"}), 400

    try:
        add_class(tenant_id, academic_year_id, class_name, section, teacher_id)
        return jsonify({"message": "Class created successfully"}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@classes_bp.route('/classes', methods=['GET'])
@jwt_required
def get_classes_route():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    try:
        classes = get_classes_by_tenant(tenant_id)
        return jsonify(classes=classes), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@classes_bp.route('/classes/<uuid:class_id>', methods=['PUT'])
@jwt_required
def update_class_route(class_id):
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    if not tenant_id:
        return jsonify({"error": "tenant_id is required"}), 400

    academic_year_id = data.get('academic_year_id')
    class_name = data.get('class_name')
    section = data.get('section')
    teacher_id = data.get('teacher_id')

    try:
        updated = update_class(
            class_id, tenant_id, academic_year_id, class_name, section, teacher_id)
        if updated == 0:
            return jsonify({"error": "Class not found or tenant mismatch"}), 404
        return jsonify({"message": "Class updated successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500


@classes_bp.route('/classes/<uuid:class_id>', methods=['DELETE'])
@jwt_required
def delete_class_route(class_id):
    tenant_id = request.current_user_jwt_claims.get('tenant_id')

    if not tenant_id:
        return jsonify({"error": "tenant_id missing from JWT"}), 400

    try:
        deleted = delete_class(class_id, tenant_id)
        if deleted == 0:
            return jsonify({"error": "Class not found or tenant mismatch"}), 404
        return jsonify({"message": "Class deleted successfully"}), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
