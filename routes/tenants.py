from flask import Blueprint, request, jsonify
from database.database import get_db_connection
from extension import Bcrypt
from utils.decorators import jwt_required
from datetime import datetime, timedelta, timezone

tenant_bp = Blueprint('tenants', __name__)


@tenant_bp.route('/tenants', methods=['GET'])
@jwt_required
def tenants():
    user_claims = request.current_user_jwt_claims
    conn = get_db_connection()
    if not conn:
        return jsonify({"error": "Failed to connect to the database."}), 500

    cur = conn.cursor()
    try:
        if user_claims.get("is_admin"):
            cur.execute("""
                SELECT id, tenant_name, address, city, country, established_date, email, phone, registration_number, is_active, created_at,password_hash
                FROM Tenants
                ORDER BY created_at DESC
            """)
        else:
            # Non-admins only see their own tenant
            cur.execute("""
                SELECT id, tenant_name, address, city, country, established_date, email, phone, registration_number, is_active, created_at,password_hash
                FROM Tenants
                WHERE id = %s
            """, (user_claims.get("tenant_id"),))

        tenants_data = cur.fetchall()
        tenants_list = []
        for tenant in tenants_data:
            tenants_list.append({
                "id": tenant[0],
                "tenant_name": tenant[1],
                "address": tenant[2],
                "city": tenant[3],
                "country": tenant[4],
                "established_date": tenant[5].strftime('%Y-%m-%d') if tenant[5] else None,
                "email": tenant[6],
                "phone": tenant[7],
                "registration_number": tenant[8],
                "is_active": tenant[9],
                "created_at": tenant[10].strftime('%Y-%m-%d %H:%M:%S') if tenant[10] else None,
                "password_hash": tenant[11]
            })

        return jsonify(tenants=tenants_list), 200

    except Exception as e:
        print(f"Error fetching tenants: {e}")
        return jsonify({"error": f"Error fetching tenants: {str(e)}"}), 500

    finally:
        cur.close()
        conn.close()


@tenant_bp.route('/tenants/update/<uuid:tenant_id>', methods=['PUT'])
@jwt_required  # Added decorator
# @admin_required  # Added decorator
def update_tenant(tenant_id):
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
    is_active = data.get('is_active')

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
            UPDATE Tenants SET
            tenant_name=%s,
            address=%s,
            city=%s,
            country=%s,
            established_date=%s,
            email=%s,
            phone=%s,
            registration_number=%s,
            is_active=%s
            WHERE id=%s
        """, (tenant_name, address, city, country, established_date, email, phone, registration_number, is_active, str(tenant_id)))

        conn.commit()
        # Corrected flash message
        return jsonify({"message": "Tenant updated successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error updating tenant: {e}"}), 500
    finally:
        cur.close()
        conn.close()


@tenant_bp.route("/tenants/delete/<uuid:tenant_id>", methods=["DELETE"])
@jwt_required  # Added decorator
# @admin_required  # Added decorator
def delete_tenant(tenant_id):

    conn = get_db_connection()

    if not conn:
        return jsonify({"error": "Database connection failed"}), 500
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Tenants WHERE id=%s", (tenant_id,))
        conn.commit()
        return jsonify({"message": "Tenant updated successfully"}), 200

    except Exception as e:
        conn.rollback()
        return jsonify({"error": f"Error updating tenant: {e}"}), 500
    finally:
        cur.close()
        conn.close()
