from database.database import get_db_connection


def create_user_role(user_id, role_id, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO UserRoles (user_id, role_id, tenant_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (user_id, role_id, tenant_id) DO NOTHING
        """, (user_id, role_id, tenant_id))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def get_all_user_roles():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT 
                ur.id,
                u.username,
                r.role_name,
                t.tenant_name
            FROM UserRoles ur
            JOIN Users u ON ur.user_id = u.id
            JOIN Roles r ON ur.role_id = r.id
            JOIN Tenants t ON ur.tenant_id = t.id
        """)
        rows = cur.fetchall()
        result = [
            {
                "id": row[0],
                "username": row[1],
                "role_name": row[2],
                "tenant_name": row[3]
            }
            for row in rows
        ]
        return result, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def update_user_role(id, user_id, role_id, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE UserRoles 
            SET user_id = %s, role_id = %s, tenant_id = %s
            WHERE id = %s
        """, (user_id, role_id, tenant_id, str(id)))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def delete_user_role(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM UserRoles WHERE id = %s", (str(id),))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()
