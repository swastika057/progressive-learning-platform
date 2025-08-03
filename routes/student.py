from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


student = Blueprint('Student', __name__)


@student.route('/students/add', methods=['POST'])
@jwt_required
# @admin_required
def add_student():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    user_id = data.get('user_id')  # Required: user_id must already exist
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    roll_no = data.get('roll_no')
    date_of_birth = data.get('date_of_birth')  # Optional but recommended
    address = data.get('address')
    parent_name = data.get('parent_name')
    parent_contact = data.get('parent_contact')
    enrollment_date = data.get('enrollment_date')

    if not user_id or not tenant_id or not roll_no:
        return jsonify({"error": "user_id, tenant_id, and roll_no are required."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Students (user_id, tenant_id, roll_no, date_of_birth, address, parent_name, parent_contact, enrollment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, tenant_id, roll_no, date_of_birth, address, parent_name, parent_contact, enrollment_date))
        conn.commit()
        return jsonify({"message": "Student added successfully!"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


# -------------------- GET ALL STUDENTS --------------------
@student.route('/students', methods=['GET'])
@jwt_required
# @admin_required
def get_students():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT * FROM Students
        """)
        students = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        result = [dict(zip(cols, row)) for row in students]
        return jsonify(students=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# -------------------- UPDATE STUDENT --------------------
@student.route('/students/update/<uuid:user_id>', methods=['PUT'])
@jwt_required
# @admin_required
def update_student(user_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')

    roll_no = data.get('roll_no')
    date_of_birth = data.get('date_of_birth')
    address = data.get('address')
    parent_name = data.get('parent_name')
    parent_contact = data.get('parent_contact')
    enrollment_date = data.get('enrollment_date')

    if not tenant_id:
        return jsonify({"error": "tenant_id is required."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed"}), 500

    try:
        cur = conn.cursor()

        cur.execute("""
            UPDATE Students SET
            roll_no = COALESCE(%s, roll_no),
            date_of_birth = COALESCE(%s, date_of_birth),
            address = COALESCE(%s, address),
            parent_name = COALESCE(%s, parent_name),
            parent_contact = COALESCE(%s, parent_contact),
            enrollment_date = COALESCE(%s, enrollment_date)
            WHERE user_id = %s AND tenant_id = %s
        """, (roll_no, date_of_birth, address, parent_name, parent_contact, enrollment_date, str(user_id), str(tenant_id)))

        if cur.rowcount == 0:
            return jsonify({"error": "Student not found or tenant mismatch"}), 404

        conn.commit()
        return jsonify({"message": "Student updated successfully!"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
