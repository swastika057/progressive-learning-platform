from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


employees_bp = Blueprint('employees', __name__)


@employees_bp.route('/employees', methods=['GET'])
@jwt_required
# @admin_required
def get_employee():
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
                SELECT * FROM Employees
            """)
        employees = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        result = [dict(zip(cols, row)) for row in employees]
        return jsonify(employees=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@employees_bp.route('/employees', methods=['POST'])
@jwt_required
# @admin_required
def create_employee():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid json"}), 400
    user_id = data.get('user_id')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    department = data.get('department')
    hire_date = data.get('hire_date')
    qualifications = data.get('qualifications')
    if not user_id or not tenant_id:
        return jsonify({"error": "user_id and tenant_id are required!"}), 400
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed!"}), 500
    try:
        cur = conn.cursor()
        cur.execute("INSERT INTO Employees( user_id, tenant_id, department, hire_date, qualifications)VALUES( %s, %s, %s, %s, %s)",
                    (user_id, tenant_id, department, hire_date, qualifications))

        conn.commit()
        return jsonify({"message": "Employee added successfully!"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@employees_bp.route('/employees/<uuid:id>', methods=['PUT'])
@jwt_required
def update_employee(id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid json"}), 400

    user_id = data.get('user_id')
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    department = data.get('department')
    hire_date = data.get('hire_date')
    qualifications = data.get('qualifications')

    if not user_id or not tenant_id:
        return jsonify({"error": "user_id and tenant_id are required!"}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed!"}), 500

    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE employees
            SET user_id = %s,
                tenant_id = %s,
                department = %s,
                hire_date = %s,
                qualifications = %s
            WHERE id = %s
            """,
            (user_id, tenant_id, department, hire_date, qualifications, id)
        )
        conn.commit()
        return jsonify({"message": "Employee updated successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@employees_bp.route('/employees/<uuid:id>', methods=['DELETE'])
@jwt_required
def employee_delete(id):
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Database connection failed!"}), 500

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM employees WHERE id = %s", (id,))
        conn.commit()
        return jsonify({"message": "Employee deleted successfully!"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
