from database.database import get_db_connection


def get_all_permissions(tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT id, permission_name, description 
            FROM Permissions
            WHERE tenant_id = %s
        """, (tenant_id,))
        permissions = cur.fetchall()
        result = [{"id": p[0], "permission_name": p[1],
                   "description": p[2]} for p in permissions]
        return result, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def create_permission(permission_name, description, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Permissions (permission_name, description, tenant_id)
            VALUES (%s, %s, %s)
            ON CONFLICT (permission_name, tenant_id) DO NOTHING
        """, (permission_name, description, tenant_id))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def update_permission_by_id(permission_id, permission_name, description, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Permissions
            SET permission_name = %s, description = %s
            WHERE id = %s AND tenant_id = %s
        """, (permission_name, description, str(permission_id), tenant_id))

        if cur.rowcount == 0:
            return False, None, True  # not found

        conn.commit()
        return True, None, False
    except Exception as e:
        conn.rollback()
        return False, str(e), False
    finally:
        cur.close()
        conn.close()


def delete_permission_by_id(permission_id, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Permissions
            WHERE id = %s AND tenant_id = %s
        """, (str(permission_id), tenant_id))

        if cur.rowcount == 0:
            return False, None, True  # not found

        conn.commit()
        return True, None, False
    except Exception as e:
        conn.rollback()
        return False, str(e), False
    finally:
        cur.close()
        conn.close()
