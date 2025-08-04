from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

subjects_bp = Blueprint('subjects', __name__)


@subjects_bp.route('/subjects', methods=['POST'])
@jwt_required
def add_subject():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    subject_name = data.get('subject_name')
    description = data.get('description')

    if not subject_name or not tenant_id:
        return jsonify({"error": "subject_name and tenant_id are required"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Subjects (tenant_id, subject_name, description)
            VALUES (%s, %s, %s)
        """, (tenant_id, subject_name, description))
        conn.commit()
        return jsonify({"message": "Subject added successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@subjects_bp.route('/subjects', methods=['GET'])
@jwt_required
def get_subjects():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT subject_id, subject_name, description
            FROM Subjects
            WHERE tenant_id = %s
            ORDER BY subject_name
        """, (tenant_id,))
        subjects = cur.fetchall()

        cols = [desc[0] for desc in cur.description]
        result = [dict(zip(cols, row)) for row in subjects]

        return jsonify(subjects=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@subjects_bp.route('/subjects/<uuid:id>', methods=['PUT'])
@jwt_required
def update_subject(id):
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    subject_name = data.get('subject_name')
    description = data.get('description')

    if not subject_name or not tenant_id:
        return jsonify({"error": "subject_name and tenant_id are required"}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Subjects
            SET tenant_id = %s, subject_name = %s, description = %s
            WHERE subject_id = %s
        """, (tenant_id, subject_name, description, str(id)))
        conn.commit()
        return jsonify({"message": "Subject updated successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@subjects_bp.route('/subjects/<uuid:id>', methods=['DELETE'])
@jwt_required
def del_subject(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database!"}), 400

    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Subjects WHERE subject_id = %s
        """, (str(id),))
        conn.commit()
        return jsonify({"message": "Subject deleted successfully"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
