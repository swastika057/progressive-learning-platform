from database.database import get_db_connection
from datetime import datetime


def register_tenant(data):
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
            return {"error": "Invalid format for established_date. Use YYYY-MM-DD."}, 400

    if not tenant_name or not email or not address:
        return {"error": "tenant_name, email, and address are required."}, 400

    conn = get_db_connection()
    if not conn:
        return {"error": "Failed to connect to database."}, 500

    cur = conn.cursor()
    try:
        # Check if tenant with email exists
        cur.execute("SELECT id FROM Tenants WHERE email = %s", (email,))
        if cur.fetchone():
            return {"error": "Tenant with this email already exists."}, 409

        # Insert new tenant
        cur.execute("""
            INSERT INTO Tenants (
                tenant_name, address, city, country,
                established_date, email, phone, registration_number
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id
        """, (tenant_name, address, city, country, established_date, email, phone, registration_number))

        tenant_id = cur.fetchone()[0]
        conn.commit()
        return {"message": "Tenant registered successfully!", "tenant_id": tenant_id}, 201

    except Exception as e:
        conn.rollback()
        return {"error": f"Error adding tenant: {str(e)}"}, 500

    finally:
        cur.close()
        conn.close()
