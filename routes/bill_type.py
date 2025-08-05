from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from utils.decorators import jwt_required
from datetime import datetime

billtypes_bp = Blueprint("bill_type", __name__)


@billtypes_bp.route('/billtypes', methods=['POST'])
@jwt_required
def add_bill_type():
    data = request.get_json()
    tenant_id = data.get('tenant_id')
    bill_type_name = data.get('bill_type_name')
    description = data.get('description')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO BillTypes (tenant_id, bill_type_name, description)
            VALUES (%s, %s, %s)
            RETURNING bill_type_id
        """, (tenant_id, bill_type_name, description))
        bill_type_id = cur.fetchone()[0]

        conn.commit()
        return jsonify({"message": "Bill type added successfully", "bill_type_id": bill_type_id}), 201
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Read all bill types for a tenant


@billtypes_bp.route('/billtypes/<tenant_id>', methods=['GET'])
@jwt_required()
def get_bill_types(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT bill_type_id, bill_type_name, description
            FROM BillTypes
            WHERE tenant_id = %s
        """, (tenant_id,))
        billtypes = cur.fetchall()

        result = []
        for bt in billtypes:
            result.append({
                "bill_type_id": bt[0],
                "bill_type_name": bt[1],
                "description": bt[2]
            })

        return jsonify(result)
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Update a bill type


@billtypes_bp.route('/billtypes/<uuid:bill_type_id>', methods=['PUT'])
@jwt_required()
def update_bill_type(bill_type_id):
    data = request.get_json()
    bill_type_name = data.get('bill_type_name')
    description = data.get('description')

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE BillTypes
            SET bill_type_name = %s, description = %s
            WHERE bill_type_id = %s
        """, (bill_type_name, description, bill_type_id))

        conn.commit()
        return jsonify({"message": "Bill type updated successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()

# Delete a bill type


@billtypes_bp.route('/billtypes/<uuid:bill_type_id>', methods=['DELETE'])
@jwt_required()
def delete_bill_type(bill_type_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM BillTypes WHERE bill_type_id = %s",
                    (bill_type_id,))
        conn.commit()

        return jsonify({"message": "Bill type deleted successfully"})
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
