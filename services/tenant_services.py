# services/tenant_services.py
from database.database import get_db_connection
from datetime import datetime


def get_all_tenants(user_claims):
    conn = get_db_connection()
    if not conn:
        return None, "Failed to connect to the database."

    cur = conn.cursor()
    try:
        if user_claims.get("is_admin"):
            cur.execute("""
                SELECT id, tenant_name, address, city, country, established_date,
                       email, phone, registration_number, is_active, created_at
                FROM Tenants
                ORDER BY created_at DESC
            """)
        else:
            cur.execute("""
                SELECT id, tenant_name, address, city, country, established_date,
                       email, phone, registration_number, is_active, created_at
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
                "created_at": tenant[10].strftime('%Y-%m-%d %H:%M:%S') if tenant[10] else None
            })

        return tenants_list, None

    except Exception as e:
        return None, f"Error fetching tenants: {str(e)}"

    finally:
        cur.close()
        conn.close()


def update_tenant_by_id(id, data):
    try:
        established_date = None
        if data.get('established_date'):
            established_date = datetime.strptime(
                data.get('established_date'), '%Y-%m-%d').date()
    except ValueError:
        return None, "Invalid format for established_date. Use YYYY-MM-DD."

    conn = get_db_connection()
    if not conn:
        return None, "Failed to connect to database."
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
        """, (
            data.get('tenant_name'),
            data.get('address'),
            data.get('city'),
            data.get('country'),
            established_date,
            data.get('email'),
            data.get('phone'),
            data.get('registration_number'),
            data.get('is_active'),
            str(id)
        ))
        conn.commit()
        return "Tenant updated successfully", None
    except Exception as e:
        conn.rollback()
        return None, f"Error updating tenant: {str(e)}"
    finally:
        cur.close()
        conn.close()


def delete_tenant_by_id(id):
    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Tenants WHERE id=%s", (id,))
        conn.commit()
        return "Tenant deleted successfully", None
    except Exception as e:
        conn.rollback()
        return None, f"Error deleting tenant: {e}"
    finally:
        cur.close()
        conn.close()
