# services/remarks_service.py

from database.database import get_db_connection


def add_remark_service(data, recorded_by):
    tenant_id = data.get('tenant_id')
    student_id = data.get('student_id')
    subject_id = data.get('subject_id')
    comment = data.get('comment')
    semester = data.get('semester')

    if not all([tenant_id, student_id, subject_id, comment]):
        return {'error': 'Missing required fields'}, 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            INSERT INTO Remarks (tenant_id, student_id, subject_id, comment, semester, recorded_by)
            VALUES (%s, %s, %s, %s, %s, %s)
        """, (tenant_id, student_id, subject_id, comment, semester, recorded_by))
        conn.commit()
        return {'message': 'Remark added successfully'}, 201
    except Exception as e:
        conn.rollback()
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


def get_remarks_service(tenant_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            SELECT r.id, r.student_id, r.subject_id, r.comment, r.semester, r.recorded_at,
                   s.first_name || ' ' || s.last_name as student_name,
                   subj.subject_name,
                   u.first_name || ' ' || u.last_name as recorded_by_name
            FROM Remarks r
            JOIN Users s ON r.student_id = s.id
            JOIN Subjects subj ON r.subject_id = subj.id
            LEFT JOIN Users u ON r.recorded_by = u.id
            WHERE r.tenant_id = %s
            ORDER BY r.recorded_at DESC
        """, (tenant_id,))
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        results = [dict(zip(cols, row)) for row in rows]
        return {'remarks': results}, 200
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


def update_remark_service(remark_id, comment, semester):
    if not comment:
        return {'error': 'Comment is required'}, 400

    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("""
            UPDATE Remarks
            SET comment = %s, semester = %s
            WHERE id = %s
        """, (comment, semester, remark_id))
        conn.commit()
        return {'message': 'Remark updated successfully'}, 200
    except Exception as e:
        conn.rollback()
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


def delete_remark_service(remark_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Remarks WHERE id = %s", (remark_id,))
        conn.commit()
        return {'message': 'Remark deleted successfully'}, 200
    except Exception as e:
        conn.rollback()
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()
