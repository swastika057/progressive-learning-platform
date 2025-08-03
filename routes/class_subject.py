from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


class_sub = Blueprint('Class_subjects', __name__)
# --------- AcademicYears---------


@class_sub.route('/class_subject/add', methods=['POST'])
@jwt_required
# @admin_required
def add_class_subject():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    class_id = data.get('class_id')
    subject_id = data.get('subject_id')
    teacher_id = data.get('teacher_id')
    academic_year_id = data.get('academic_year_id')
    if not all([class_id, subject_id, teacher_id]):
        return jsonify({"error": "Missing required field"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed!"}), 500
    try:
        cur = conn.cursor()
        cur.execute("""INSERT INTO ClassSubjects( tenant_id, class_id, subject_id, teacher_id, academic_year_id)
        VALUES(%s, %s, %s,%s, %s)""", (tenant_id, class_id, subject_id, teacher_id, academic_year_id))

        conn.commit()
        return jsonify({"message": "Class Subject added successfully!"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@class_sub.route('/class_subjects', methods=['GET'])
@jwt_required
# @admin_required
def class_subject():
    tenant_id = request.args.get('tenant_id')
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT cs.class_subject_id, c.class_name, s.subject_name, u.first_name || ' ' ||u.last_name as teacher_name, a.year_label 
            from ClassSubjects as cs
            join Classes as c
            on cs.class_id = c.class_id
            join Subjects as s
            on cs.subject_id=s.subject_id
            join AcademicYears as a
            on a.academic_year_id = cs.academic_year_id
            join Users as u
            on u.id = cs.teacher_id
            order by a.year_label
                
        """
        cur.execute(query, (tenant_id,))
        class_subject = cur.fetchall()

        cols = [desc[0] for desc in cur.description]
        result = [dict(zip(cols, row)) for row in class_subject]

        return jsonify(class_subject=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
