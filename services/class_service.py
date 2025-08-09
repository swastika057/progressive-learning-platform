from database.database import get_db_connection


def add_class(tenant_id, academic_year_id, class_name, section, teacher_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Classes (tenant_id, academic_year_id, class_name, section, teacher_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (tenant_id, academic_year_id, class_name, section, teacher_id))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def get_classes_by_tenant(tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        query = """
            SELECT
                c.id,
                c.class_name,
                c.section,
                c.academic_year_id,
                c.teacher_id,
                u.first_name || ' ' || u.last_name AS teacher_name
            FROM Classes c
            LEFT JOIN Users u ON c.teacher_id = u.id
            WHERE c.tenant_id = %s
            ORDER BY c.class_name, c.section
        """
        cur.execute(query, (tenant_id,))
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in rows]
    finally:
        cur.close()
        conn.close()


def update_class(class_id, tenant_id, academic_year_id, class_name, section, teacher_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Classes SET
                academic_year_id = COALESCE(%s, academic_year_id),
                class_name = COALESCE(%s, class_name),
                section = COALESCE(%s, section),
                teacher_id = COALESCE(%s, teacher_id)
            WHERE class_id = %s AND tenant_id = %s
        """, (academic_year_id, class_name, section, teacher_id, str(class_id), tenant_id))
        updated = cur.rowcount
        conn.commit()
        return updated
    finally:
        cur.close()
        conn.close()


def delete_class(class_id, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Classes WHERE class_id = %s AND tenant_id = %s", (str(
            class_id), tenant_id))
        deleted = cur.rowcount
        conn.commit()
        return deleted
    finally:
        cur.close()
        conn.close()
