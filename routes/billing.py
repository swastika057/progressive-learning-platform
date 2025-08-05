from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from utils.decorators import jwt_required
from datetime import datetime

billing_bp = Blueprint('billing', __name__)

# Create new billing record


@billing_bp.route('/billing', methods=['POST'])
@jwt_required()
def add_billing():
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    student_id = data.get('student_id')
    bill_type_id = data.get('bill_type_id')
    amount = data.get('amount')
    billing_date = data.get('billing_date')
    due_date = data.get('due_date')
    status = data.get('status')
    description = data.get('description')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Billing (tenant_id, student_id, bill_type_id, amount, billing_date, due_date, status, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING billing_id
        """, (tenant_id, student_id, bill_type_id, amount, billing_date, due_date, status, description))
        billing_id = cur.fetchone()[0]
        conn.commit()

        return jsonify({"message": "Billing record added", "billing_id": billing_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Get all billing records for a tenant
@billing_bp.route('/billing/<uuid:tenant_id>', methods=['GET'])
@jwt_required()
def get_billing_by_tenant(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT billing_id, student_id, bill_type_id, amount, billing_date, due_date, status, description
            FROM Billing
            WHERE tenant_id = %s
        """, (tenant_id,))
        billings = cur.fetchall()

        results = []
        for row in billings:
            results.append({
                "billing_id": row[0],
                "student_id": row[1],
                "bill_type_id": row[2],
                "amount": float(row[3]),
                "billing_date": str(row[4]),
                "due_date": str(row[5]) if row[5] else None,
                "status": row[6],
                "description": row[7]
            })

        return jsonify(results)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Update billing record
@billing_bp.route('/billing/<uuid:billing_id>', methods=['PUT'])
@jwt_required()
def update_billing(billing_id):
    data = request.get_json()
    amount = data.get('amount')
    due_date = data.get('due_date')
    status = data.get('status')
    description = data.get('description')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Billing
            SET amount = %s, due_date = %s, status = %s, description = %s
            WHERE billing_id = %s
        """, (amount, due_date, status, description, billing_id))
        conn.commit()

        return jsonify({"message": "Billing record updated"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


# Delete billing record
@billing_bp.route('/billing<uuid:billing_id>', methods=['DELETE'])
@jwt_required()
def delete_billing(billing_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Billing WHERE billing_id = %s", (billing_id,))
        conn.commit()

        return jsonify({"message": "Billing record deleted"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
