from database.database import get_db_connection


def get_permissions_for_role(role_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT rp.id, r.role_name, p.id AS permission_id, p.permission_name, p.description
            FROM RolePermissions rp
            JOIN Roles r ON rp.role_id = r.id
            JOIN Permissions p ON rp.permission_id = p.id
            WHERE r.id = %s
            ORDER BY r.role_name
        """, (str(role_id),))

        perms = cur.fetchall()
        result = [{
            "id": p[0],
            "role_name": p[1],
            "permission_id": p[2],
            "permission_name": p[3],
            "description": p[4]
        } for p in perms]
        return result, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def assign_permission_to_role(role_id, permission_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO RolePermissions (role_id, permission_id)
            VALUES (%s, %s)
            ON CONFLICT (role_id, permission_id) DO NOTHING
        """, (role_id, permission_id))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def update_role_permission(role_permission_id, role_id, permission_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE RolePermissions
            SET role_id = %s, permission_id = %s
            WHERE id = %s
        """, (role_id, permission_id, str(role_permission_id)))
        conn.commit()
        return True, None
    except Exception as e:
        conn.rollback()
        return False, str(e)
    finally:
        cur.close()
        conn.close()


def delete_role_permission_by_id(role_permission_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM RolePermissions WHERE id = %s",
                    (str(role_permission_id),))
        if cur.rowcount == 0:
            return False, None, True  # Not found
        conn.commit()
        return True, None, False
    except Exception as e:
        conn.rollback()
        return False, str(e), False
    finally:
        cur.close()
        conn.close()
