from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import bcrypt
from utils.jwt_handler import create_jwt_token
from utils.decorators import admin_required
from psycopg2.extras import RealDictCursor
from datetime import datetime, timedelta, timezone


register = Blueprint('register', __name__)


@register.route('/tenants/register', methods=['POST'])
@admin_required  # Added decorator
def register_tenants():
    # user_claims already checked by admin_required
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400
    tenant_name = data.get('tenant_name')
    address = data.get('address')
    city = data.get('city')
    country = data.get('country')
    email = data.get('email')
    phone = data.get('phone')
    registration_number = data.get('registration_number')

    established_date_str = data.get('established_date')
    established_date = None
    if established_date_str:
        try:
            established_date = datetime.strptime(
                established_date_str, '%Y-%m-%d').date()
        except ValueError:
            return jsonify({"error": "Invalid format for established_date. Use YYYY-MM-DD."}), 400

    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to database."}), 500
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Tenants (tenant_name, address, city, country, established_date, email, phone, registration_number)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (tenant_name, address, city, country, established_date, email, phone, registration_number))

        conn.commit()
        return jsonify({"message": "Tenant register successfully!"}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error adding tenant: {str(e)}"}), 500

    finally:
        cur.close()
        conn.close()
