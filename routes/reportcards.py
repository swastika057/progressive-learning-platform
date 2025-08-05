from flask import Blueprint, request, jsonify
from database import get_db_connection
from utils.decorators import jwt_required
from datetime import datetime

report_card_bp = Blueprint('report_cards', __name__)

# CREATE


@report_card_bp.route('/report_cards/add', methods=['POST'])
@jwt_required()
def add_report_card():
    data = request.get_json()

    required_fields = ['tenant_id', 'student_id',
                       'academic_year_id', 'semester']
    if not all(field in data for field in required_fields):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO ReportCards (
                tenant_id, student_id, academic_year_id, semester,
                issue_date, overall_comment, issued_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING report_card_id;
        """, (
            data['tenant_id'], data['student_id'], data['academic_year_id'], data['semester'],
            data.get('issue_date'), data.get(
                'overall_comment'), data.get('issued_by')
        ))

        new_id = cur.fetchone()[0]
        conn.commit()
        cur.close()
        conn.close()

        return jsonify({'message': 'Report card added successfully', 'report_card_id': new_id}), 201

    except Exception as e:
        return jsonify({'error': str(e)}), 500


# READ (All or by student)
@grades_bp.route('/grades', methods=['GET'])
@jwt_required()
def get_all_grades():
    conn = get_db_connection()
    cursor = conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor)

    query = """
        SELECT 
            sg.id,
            sg.student_id,
            u.full_name AS student_name,
            s.year_level,
            t.name AS tenant_name,
            sg.indicator_item_id,
            sg.milestone,
            sg.grade_date,
            sg.semester
        FROM Student_Grades sg
        JOIN Students s ON sg.student_id = s.user_id
        JOIN Users u ON s.user_id = u.id
        JOIN Tenants t ON sg.tenant_id = t.id
    """

    cursor.execute(query)
    grades = cursor.fetchall()

    cursor.close()
    conn.close()

    return jsonify(grades), 200


# UPDATE
@report_card_bp.route('/report_cards/<uuid:report_card_id>', methods=['PUT'])
@jwt_required()
def update_report_card(report_card_id):
    data = request.get_json()
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE ReportCards SET
                semester = %s,
                issue_date = %s,
                overall_comment = %s,
                issued_by = %s
            WHERE report_card_id = %s;
        """, (
            data.get('semester'), data.get(
                'issue_date'), data.get('overall_comment'),
            data.get('issued_by'), str(report_card_id)
        ))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Report card updated successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500


# DELETE
@report_card_bp.route('/report_cards/<uuid:report_card_id>', methods=['DELETE'])
@jwt_required()
def delete_report_card(report_card_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM ReportCards WHERE report_card_id = %s;", (str(report_card_id),))
        conn.commit()
        cur.close()
        conn.close()
        return jsonify({'message': 'Report card deleted successfully'})
    except Exception as e:
        return jsonify({'error': str(e)}), 500
