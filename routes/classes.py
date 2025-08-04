from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


classes_bp = Blueprint('classes', __name__)
# ---------CLASSES--------


@classes_bp.route('/classes', methods=['POST'])
@jwt_required
# @admin_required
def add_class():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    academic_year_id = data.get('academic_year_id')
    class_name = data.get('class_name')
    section = data.get('section')
    teacher_id = data.get('teacher_id')

    if not all([tenant_id, academic_year_id, class_name]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Classes (tenant_id, academic_year_id, class_name, section, teacher_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (tenant_id, academic_year_id, class_name, section, teacher_id))
        conn.commit()
        return jsonify({"message": "Class created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@classes_bp .route('/classes', methods=['GET'])
@jwt_required
# @admin_required
def get_classes():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT
                c.class_id,
                c.class_name,
                c.section,
                c.academic_year_id,
                c.teacher_id,
                u.first_name || ' ' || u.last_name AS teacher_name
            FROM Classes c
            LEFT JOIN Users u ON c.teacher_id = u.id
          
            ORDER BY c.class_name, c.section
        """
        cur.execute(query, (tenant_id,))
        classes = cur.fetchall()

        cols = [desc[0] for desc in cur.description]
        result = [dict(zip(cols, row)) for row in classes]

        return jsonify(classes=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
