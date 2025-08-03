from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


employees = Blueprint('Employees', __name__)


@employees.route('/employees', methods=['GET'])
@jwt_required
# @admin_required
def employee():
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


@employees.route('/employees/update/<uuid:id>', methods=['POST'])
@jwt_required
# @admin_required
def update_employee():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid json"})
    employee_id = data.get('employee_id')
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


@employees.route('/employees/delete/<uuid:employee_id>', methods=['DELETE'])
@jwt_required
# @admin_required
def employee_delete(employee_id):
    conn = get_db_connection
    try:
        cur = conn.cursor()
        cur.execute("DELETE * from employees where id=%s", (employee_id))
        cur.commit()
        return jsonify({"message": "Employees deleted successfully!"}), 201

    except Exception as e:
        cur.rollback()
        return jsonify({"error": str(e)})

    finally:
        cur.commit()
        conn.commit()
