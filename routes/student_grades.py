from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from utils.decorators import jwt_required
import uuid

student_grades_bp = Blueprint('student_grades', __name__)


@student_grades_bp.route('/student-grades', methods=['POST'])
@jwt_required
def add_student_grade():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    student_id = data.get('student_id')
    indicator_item_id = data.get('indicator_item_id')
    milestone = data.get('milestone')
    grade_date = data.get('grade_date')
    semester = data.get('semester')
    academic_year_id = data.get('academic_year_id')
    recorded_by = data.get('recorded_by')

    if not all([tenant_id, student_id, indicator_item_id, milestone, grade_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
                INSERT INTO Student_Grades (
                    tenant_id, student_id, indicator_item_id, milestone, grade_date, semester, academic_year_id, recorded_by
                )
                VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            """, (
            tenant_id, student_id, indicator_item_id, milestone, grade_date, semester, academic_year_id, recorded_by
        ))

        conn.commit()
        return jsonify({"message": "Student grade created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@student_grades_bp.route('/student-grades', methods=['GET'])
@jwt_required
def get_student_grades():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        query = """
            SELECT sg.id, sg.student_id, sg.indicator_item_id, sg.milestone, sg.grade_date, sg.semester,
                   sg.academic_year_id, sg.recorded_by
            FROM Student_Grades sg
            WHERE sg.tenant_id = %s
            ORDER BY sg.grade_date DESC
        """
        cur.execute(query, (tenant_id,))
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        grades = [dict(zip(cols, row)) for row in rows]

        return jsonify(student_grades=grades), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@student_grades_bp.route('/student-grades/<grade_id>', methods=['PUT'])
@jwt_required
def update_student_grade(grade_id):
    data = request.get_json()
    milestone = data.get('milestone')
    grade_date = data.get('grade_date')
    semester = data.get('semester')
    academic_year_id = data.get('academic_year_id')
    recorded_by = data.get('recorded_by')

    if not all([milestone, grade_date]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Student_Grades SET milestone=%s, grade_date=%s, semester=%s, academic_year_id=%s, recorded_by=%s
            WHERE id=%s
        """, (
            milestone, grade_date, semester, academic_year_id, recorded_by, grade_id
        ))
        conn.commit()
        return jsonify({"message": "Student grade updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@student_grades_bp.route('/student-grades/<grade_id>', methods=['DELETE'])
@jwt_required
def delete_student_grade(grade_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Student_Grades WHERE id = %s", (grade_id,))
        conn.commit()
        return jsonify({"message": "Student grade deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
