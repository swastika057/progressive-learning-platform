from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from flask_bcrypt import Bcrypt
from extension import bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone


academic_years = Blueprint('Academic_years', __name__)
# --------- AcademicYears---------


@academic_years.route('/academic_years', methods=['GET'])
@jwt_required
# @admin_required
def get_academic_years():
    tenant_id = request.args.get(
        'tenant_id') or request.current_user_jwt_claims.get("tenant_id")
    # Get year from query param

    conn = get_db_connection()
    try:
        cur = conn.cursor()
        # if year_filter:
        #     cur.execute("""
        #         SELECT * FROM AcademicYears
        #         WHERE tenant_id = %s AND year_label = %s
        #     """, (tenant_id, year_filter))
        # else:
        cur.execute("""
                SELECT * FROM AcademicYears
           
            """, (tenant_id,))
        years = cur.fetchall()
        print("years:", years)

        cols = [desc[0] for desc in cur.description]
        result = [dict(zip(cols, row)) for row in years]

        return jsonify(years=result), 200
    except Exception as e:
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()


@academic_years.route('/AcademicYears/add', methods=['POST'])
@jwt_required
# @admin_required
def add_AcademicYears():
    data = request.get_json()
    tenant_id = data.get(
        'tenant_id') or request.current_user_jwt_claims.get('tenant_id')
    year_label = data.get('year_label')

    if not all([tenant_id]):
        return jsonify({"error": "Missing required fields"}), 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO AcademicYears (tenant_id, year_label)
            VALUES (%s, %s)ON CONFLICT (year_label, tenant_id) DO NOTHING
            RETURNING academic_year_id
        """, (tenant_id, year_label))

        academic_year_id = cur.fetchone()
        print("Inserted academic_year_id:", academic_year_id)
        conn.commit()
        return jsonify({"message": "AcademicYears created successfully"}), 201
    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500
    finally:
        cur.close()
        conn.close()
