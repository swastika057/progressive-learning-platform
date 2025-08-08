from database.database import get_db_connection


def get_all_academic_years(tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM AcademicYears WHERE tenant_id = %s
        """, (tenant_id,))
        years = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in years]
    finally:
        cur.close()
        conn.close()


def create_academic_year(tenant_id, year_label):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO AcademicYears (tenant_id, year_label)
            VALUES (%s, %s)
            ON CONFLICT (year_label, tenant_id) DO NOTHING
            RETURNING id
        """, (tenant_id, year_label))
        conn.commit()
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def update_academic_year(year_id, year_label):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE AcademicYears
            SET year_label = %s
            WHERE id = %s
        """, (year_label, year_id))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()


def delete_academic_year(year_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM AcademicYears WHERE id = %s", (year_id,))
        conn.commit()
        return cur.rowcount > 0
    except Exception as e:
        conn.rollback()
        raise e
    finally:
        cur.close()
        conn.close()
