from database.database import get_db_connection
from extension import bcrypt
from psycopg2.extras import RealDictCursor

SUPERADMIN_EMAIL = 'superadmin@example.com'


def authenticate_user(email: str, password: str):
    if not email or not password:
        return None, "Email and password are required"

    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT id, username, email, password_hash, tenant_id
            FROM Users WHERE email = %s AND is_active = TRUE
        """, (email,))
        user = cur.fetchone()

        if not user:
            return None, "Invalid email or password"

        if not bcrypt.check_password_hash(user['password_hash'], password):
            return None, "Invalid email or password"

        cur.execute("""
            SELECT R.role_name FROM UserRoles UR
            JOIN Roles R ON UR.role_id = R.id
            WHERE UR.user_id = %s AND UR.tenant_id = %s
        """, (user['id'], user['tenant_id']))
        roles = [row['role_name'] for row in cur.fetchall()]

        if not roles and email.lower() == SUPERADMIN_EMAIL.lower():
            roles = ['superadmin']

        # Prepare user data to generate token
        user_data = {
            'user_id': str(user['id']),
            'username': user['username'],
            'email': user['email'],
            'tenant_id': str(user['tenant_id']),
            'roles': roles
        }
        return user_data, None

    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()
