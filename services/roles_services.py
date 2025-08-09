from database.database import get_db_connection


def fetch_roles():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute(
            """SELECT id, role_name, tenant_id, description FROM roles""")
        roles_data = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in roles_data], None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def create_role(role_name, description, tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("""
            INSERT INTO roles (role_name, description, tenant_id)
            VALUES (%s, %s, %s)
        """, (role_name, description, tenant_id))

        conn.commit()
        cur.close()
        conn.close()

        return "Role created successfully", None
    except Exception as e:
        return None, str(e)


def update_role_by_id(role_id, role_name, description, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Roles
            SET role_name = %s, description = %s
            WHERE tenant_id = %s AND id = %s
        """, (role_name, description, str(tenant_id), str(role_id)))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def delete_role_by_id(role_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM roles WHERE id = %s", (str(role_id),))
        conn.commit()
        return True
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
