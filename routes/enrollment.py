from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

enrollment_bp = Blueprint('enrollment', __name__)


@enrollment_bp.route('/enrollment', methods=['POST'])
@jwt_required
def add_enrollment():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid json"}), 400
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    student_id = data.get('student_id')
    class_id = data.get('class_id')
    academic_year_id = data.get('academic_year_id')
    enrollment_date = data.get('enrollment_date')

    # Validate required fields
    if not all([student_id, class_id, academic_year_id, tenant_id]):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Enrollments (tenant_id, student_id, class_id, academic_year_id, enrollment_date)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (student_id, class_id, academic_year_id, tenant_id) DO NOTHING
        """, (tenant_id, student_id, class_id, academic_year_id, enrollment_date))
        conn.commit()
        return jsonify({"message": "Enrollment added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@enrollment_bp.route('/enrollments', methods=['GET'])
@jwt_required
def get_enrollments():
    tenant_id = request.current_user_jwt_claims.get("tenant_id")

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT
                e.id,
                e.student_id,
                u.first_name || ' ' || u.last_name AS student_name,
                c.id AS class_id,
                c.class_name,
                c.section,
                ay.id AS academic_year_id,
                ay.year_label,
                e.enrollment_date
            FROM Enrollments e
            JOIN Students s ON e.student_id = s.user_id
            JOIN Users u ON s.user_id = u.id
            JOIN Classes c ON e.class_id = c.id
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            WHERE e.tenant_id = %s
        """, (tenant_id,))

        rows = cur.fetchall()

        enrollments = []
        for row in rows:
            enrollments.append({
                "enrollment_id": row[0],
                "student_id": row[1],
                "student_name": row[2],
                "class_id": row[3],
                "class_name": row[4],
                "section": row[5],
                "academic_year_id": row[6],
                "academic_year": row[7],
                "enrollment_date": row[8].isoformat() if row[8] else None
            })

        return jsonify(enrollments), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@enrollment_bp.route('/enrollments/<uuid:enrollment_id>', methods=['PUT'])
@jwt_required
def update_enrollment(enrollment_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    data = request.get_json()

    class_id = data.get("class_id")
    academic_year_id = data.get("academic_year_id")
    enrollment_date = data.get("enrollment_date")

    if not (class_id and academic_year_id):
        return jsonify({"error": "Missing required fields"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Enrollments
            SET class_id = %s,
                academic_year_id = %s,
                enrollment_date = %s
            WHERE id = %s AND tenant_id = %s
        """, (class_id, academic_year_id, enrollment_date, enrollment_id, tenant_id))

        if cur.rowcount == 0:
            return jsonify({"error": "Enrollment not found or unauthorized"}), 404

        conn.commit()
        return jsonify({"message": "Enrollment updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@enrollment_bp.route('/enrollments/<uuid:enrollment_id>', methods=['DELETE'])
@jwt_required
def delete_enrollment(enrollment_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Enrollments
            WHERE id = %s AND tenant_id = %s
        """, (enrollment_id, tenant_id))

        if cur.rowcount == 0:
            return jsonify({"error": "Enrollment not found or unauthorized"}), 404

        conn.commit()
        return jsonify({"message": "Enrollment deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
