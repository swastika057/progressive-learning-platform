from database.database import get_db_connection


def add_subject(data, tenant_id):
    subject_name = data.get('subject_name')
    description = data.get('description')

    if not subject_name or not tenant_id:
        return None, "subject_name and tenant_id are required", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Subjects (tenant_id, subject_name, description)
            VALUES (%s, %s, %s)
        """, (tenant_id, subject_name, description))
        conn.commit()
        return "Subject added successfully", None, 201
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def get_subjects(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, subject_name, description
            FROM Subjects
            WHERE tenant_id = %s
            ORDER BY subject_name
        """, (tenant_id,))
        subjects = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        result = [dict(zip(cols, row)) for row in subjects]
        return result, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def update_subject(subject_id, tenant_id, data):
    subject_name = data.get('subject_name')
    description = data.get('description')

    if not subject_name or not tenant_id:
        return None, "subject_name and tenant_id are required", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Subjects
            SET subject_name = %s, description = %s
            WHERE subject_id = %s AND tenant_id = %s
        """, (subject_name, description, str(subject_id), tenant_id))
        if cur.rowcount == 0:
            return None, "Subject not found or unauthorized", 404
        conn.commit()
        return "Subject updated successfully", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def delete_subject(subject_id, tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Subjects WHERE subject_id = %s AND tenant_id = %s
        """, (str(subject_id), tenant_id))
        if cur.rowcount == 0:
            return None, "Subject not found or unauthorized", 404
        conn.commit()
        return "Subject deleted successfully", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()
