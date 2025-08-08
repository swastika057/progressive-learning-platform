from database.database import get_db_connection
from extension import bcrypt
from psycopg2.extras import RealDictCursor
from datetime import datetime


def fetch_users(is_admin, tenant_id):
    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cur = conn.cursor(cursor_factory=RealDictCursor)
        if is_admin and not tenant_id:
            cur.execute("SELECT * FROM Users")
        else:
            if not tenant_id:
                return None, "Missing tenant_id for non-admin user"
            cur.execute(
                """SELECT id, username, email, first_name, last_name, contact_phone, tenant_id,
                          gender, date_of_birth, is_active, last_login, created_at, updated_at
                   FROM Users WHERE tenant_id = %s""",
                (str(tenant_id),)
            )
        users = cur.fetchall()
        return users, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def add_user(data):
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_phone = data.get('contact_phone')
    gender = data.get('gender')
    date_of_birth = data.get('date_of_birth')
    tenant_id = data.get('tenant_id')

    if not username or not password or not email or not tenant_id:
        return None, "Username, password, email, and tenant_id are required."

    try:
        dob_obj = datetime.strptime(
            date_of_birth, "%Y-%m-%d").date() if date_of_birth else None
    except ValueError:
        return None, "Invalid date_of_birth. Use YYYY-MM-DD."

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cur = conn.cursor()
        cur.execute(
            """
            INSERT INTO Users (username, password_hash, email, first_name, last_name,
                               contact_phone, gender, date_of_birth, tenant_id)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            """,
            (username, password_hash, email, first_name, last_name,
             contact_phone, gender, dob_obj, tenant_id)
        )
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def update_user(user_id, data):
    username = data.get('username')
    password = data.get('password')
    email = data.get('email')
    first_name = data.get('first_name')
    last_name = data.get('last_name')
    contact_phone = data.get('contact_phone')
    gender = data.get('gender')
    date_of_birth = data.get('date_of_birth')
    tenant_id = data.get('tenant_id')

    if not username or not password or not email or not tenant_id:
        return None, "Username, password, email, and tenant_id are required."

    try:
        dob_obj = datetime.strptime(
            date_of_birth, "%Y-%m-%d").date() if date_of_birth else None
    except ValueError:
        return None, "Invalid date_of_birth. Use YYYY-MM-DD."

    password_hash = bcrypt.generate_password_hash(password).decode('utf-8')

    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cur = conn.cursor()
        cur.execute(
            """
            UPDATE Users SET
                username = %s,
                password_hash = %s,
                email = %s,
                first_name = %s,
                last_name = %s,
                contact_phone = %s,
                gender = %s,
                date_of_birth = %s,
                tenant_id = %s,
                updated_at = CURRENT_TIMESTAMP
            WHERE id = %s
            """,
            (username, password_hash, email, first_name, last_name,
             contact_phone, gender, dob_obj, tenant_id, str(user_id))
        )
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def delete_user(user_id):
    conn = get_db_connection()
    if not conn:
        return None, "Database connection failed"

    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Users WHERE id = %s", (str(user_id),))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return None, str(e)
    finally:
        cur.close()
        conn.close()
