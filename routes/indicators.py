from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from utils.decorators import jwt_required

indicators_bp = Blueprint("indicators", __name__)


@indicators_bp.route('/indicators', methods=['POST'])
@jwt_required
def create_indicator():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    subject_id = data.get("subject_id")
    name = data.get("name")
    sort_order = data.get("sort_order")

    if not tenant_id or not subject_id or not name:
        return jsonify({"error": "tenant_id, subject_id, and name are required."}), 400

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Indicators (tenant_id, subject_id, name, sort_order)
            VALUES (%s, %s, %s, %s)
        """, (tenant_id, subject_id, name, sort_order))
        conn.commit()
        return jsonify({"message": "Indicator created successfully."}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@indicators_bp.route('/indicators', methods=['GET'])
@jwt_required
def get_indicators():
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Indicators WHERE tenant_id = %s
        """, (tenant_id,))
        indicators = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        results = [dict(zip(columns, row)) for row in indicators]
        return jsonify(results), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@indicators_bp.route('/indicators/<uuid:indicator_id>', methods=['PUT'])
@jwt_required
def update_indicator(indicator_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    subject_id = data.get("subject_id")
    name = data.get("name")
    sort_order = data.get("sort_order")

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Indicators SET subject_id = %s, name = %s, sort_order = %s
            WHERE id = %s AND tenant_id = %s
        """, (subject_id, name, sort_order, indicator_id, tenant_id))
        if cur.rowcount == 0:
            return jsonify({"error": "Indicator not found or unauthorized"}), 404
        conn.commit()
        return jsonify({"message": "Indicator updated successfully."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@indicators_bp.route('/indicators/<uuid:indicator_id>', methods=['DELETE'])
@jwt_required
def delete_indicator(indicator_id):
    tenant_id = request.current_user_jwt_claims.get("tenant_id")
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Indicators WHERE id = %s AND tenant_id = %s
        """, (indicator_id, tenant_id))
        if cur.rowcount == 0:
            return jsonify({"error": "Indicator not found or unauthorized"}), 404
        conn.commit()
        return jsonify({"message": "Indicator deleted successfully."}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
