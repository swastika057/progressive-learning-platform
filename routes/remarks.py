from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


remarks_bp = Blueprint("remarks", __name__)


@remarks_bp.route('/remarks', methods=['POST'])
@jwt_required
def add_remark():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    student_id = data.get('student_id')
    subject_id = data.get('subject_id')
    comment = data.get('comment')
    semester = data.get('semester')
    recorded_by = request.current_user_jwt_claims.get('user_id')

    if not all([tenant_id, student_id, subject_id, comment]):
        return jsonify({'error': 'Missing required fields'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Remarks (tenant_id, student_id, subject_id, comment, semester, recorded_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tenant_id, student_id, subject_id, comment, semester, recorded_by))
        conn.commit()
        return jsonify({'message': 'Remark added successfully'}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# --------- GET REMARKS ---------
@remarks_bp.route('/remarks', methods=['GET'])
@jwt_required
def get_remarks():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT r.id, r.student_id, r.subject_id, r.comment, r.semester, r.recorded_at,
                   s.first_name || ' ' || s.last_name as student_name,
                   subj.subject_name,
                   u.first_name || ' ' || u.last_name as recorded_by_name
            FROM Remarks r
            JOIN Users s ON r.student_id = s.id
            JOIN Subjects subj ON r.subject_id = subj.subject_id
            LEFT JOIN Users u ON r.recorded_by = u.id
            WHERE r.tenant_id = %s
            ORDER BY r.recorded_at DESC
        """, (tenant_id,))
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        results = [dict(zip(cols, row)) for row in rows]
        return jsonify(remarks=results), 200
    except Exception as e:
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# --------- UPDATE REMARK ---------
@remarks_bp.route('/remarks/<uuid:remark_id>', methods=['PUT'])
@jwt_required
def update_remark(remark_id):
    data = request.get_json()
    comment = data.get('comment')
    semester = data.get('semester')

    if not comment:
        return jsonify({'error': 'Comment is required'}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Remarks
            SET comment = %s, semester = %s
            WHERE id = %s
        """, (comment, semester, remark_id))
        conn.commit()
        return jsonify({'message': 'Remark updated successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()


# --------- DELETE REMARK ---------
@remarks_bp.route('/remarks/<uuid:remark_id>', methods=['DELETE'])
@jwt_required
def delete_remark(remark_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM Remarks WHERE id = %s", (remark_id,))
        conn.commit()
        return jsonify({'message': 'Remark deleted successfully'}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({'error': str(e)}), 500
    finally:
        cur.close()
        conn.close()
