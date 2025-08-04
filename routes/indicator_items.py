from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from utils.decorators import jwt_required

indicator_items_bp = Blueprint("indicator_items", __name__)


@indicator_items_bp.route("/indicator-items", methods=["POST"])
@jwt_required
def create_indicator_item():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    subject = data.get("subject")
    indicator = data.get("indicator")
    item = data.get("item")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Indicator_Items (tenant_id, subject, indicator, item)
            VALUES (%s, %s, %s, %s)
        """, (str(tenant_id), subject, indicator, item))

        conn.commit()
        return jsonify({"message": "Indicator item created"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@indicator_items_bp.route("/indicator-items", methods=["GET"])
@jwt_required
def get_indicator_items():
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            SELECT id, subject, indicator, item
            FROM Indicator_Items
            WHERE tenant_id = %s
        """, (str(tenant_id),))

        rows = cur.fetchall()
        result = [
            {"id": r[0], "subject": r[1], "indicator": r[2], "item": r[3]}
            for r in rows
        ]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@indicator_items_bp.route("/indicator-items/<item_id>", methods=["PUT"])
@jwt_required
def update_indicator_item(item_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    subject = data.get("subject")
    indicator = data.get("indicator")
    item = data.get("item")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Indicator_Items
            SET subject = %s, indicator = %s, item = %s
            WHERE id = %s AND tenant_id = %s
        """, (subject, indicator, item, str(item_id), str(tenant_id)))

        if cur.rowcount == 0:
            return jsonify({"error": "Indicator item not found"}), 404

        conn.commit()
        return jsonify({"message": "Indicator item updated"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


@indicator_items_bp.route("/indicator-items/<item_id>", methods=["DELETE"])
@jwt_required
def delete_indicator_item(item_id):
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            DELETE FROM Indicator_Items
            WHERE id = %s AND tenant_id = %s
        """, (str(item_id), str(tenant_id)))

        if cur.rowcount == 0:
            return jsonify({"error": "Indicator item not found"}), 404

        conn.commit()
        return jsonify({"message": "Indicator item deleted"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
