from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


milestones_bp = Blueprint("milestones", __name__)


@milestones_bp.route("/milestones", methods=["POST"])
@jwt_required
def create_milestone():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    milestone = data.get("milestone")
    description = data.get("description")

    if milestone not in ('A', 'B', 'C', 'D'):
        return jsonify({"error": "Milestone must be one of A, B, C, D"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO Milestones ( tenant_id, milestone, description)
            VALUES (%s, %s, %s)
        """, (tenant_id, milestone, description))
        conn.commit()

        return jsonify({"message": "Milestone created"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@milestones_bp.route("/milestones", methods=["GET"])
@jwt_required
def get_milestones():
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute(
            "SELECT id, milestone, description FROM Milestones WHERE tenant_id = %s", (tenant_id,))
        rows = cur.fetchall()

        milestones = [{"id": r[0], "milestone": r[1],
                       "description": r[2]} for r in rows]
        return jsonify(milestones), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@milestones_bp.route("/milestones/<milestone_id>", methods=["PUT"])
@jwt_required
def update_milestone(milestone_id):
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    tenant_id = data.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")
    description = data.get("description")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            UPDATE Milestones SET description = %s
            WHERE id = %s AND tenant_id = %s
        """, (description, milestone_id, str(tenant_id)))
        if cur.rowcount == 0:
            return jsonify({"error": "Milestone not found"}), 404

        conn.commit()
        return jsonify({"message": "Milestone updated"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@milestones_bp.route("/milestones/<milestone_id>", methods=["DELETE"])
@jwt_required
def delete_milestone(milestone_id):
    tenant_id = request.args.get(
        "tenant_id") or request.current_user_jwt_claims.get("tenant_id")

    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Milestones WHERE id = %s AND tenant_id = %s",
                    (milestone_id, str(tenant_id)))
        if cur.rowcount == 0:
            return jsonify({"error": "Milestone not found"}), 404

        conn.commit()
        return jsonify({"message": "Milestone deleted"}), 200
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
