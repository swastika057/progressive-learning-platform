# business/class_subject_business.py

from database.database import get_db_connection


def add_class_subject_logic(data, tenant_id):
    class_id = data.get('class_id')
    subject_id = data.get('subject_id')
    teacher_id = data.get('teacher_id')
    academic_year_id = data.get('academic_year_id')

    if not all([class_id, subject_id, teacher_id]):
        return {"error": "Missing required fields"}, 400

    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed!"}, 500

    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ClassSubjects(tenant_id, class_id, subject_id, teacher_id, academic_year_id)
            VALUES (%s, %s, %s, %s, %s)
        """, (tenant_id, class_id, subject_id, teacher_id, academic_year_id))
        conn.commit()
        return {"message": "Class Subject added successfully!"}, 201
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def get_all_class_subjects_logic():
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed!"}, 500

    try:
        cur = conn.cursor()
        query = """
            SELECT cs.id, c.class_name, s.subject_name,
                   u.first_name || ' ' || u.last_name AS teacher_name,
                   a.year_label
            FROM ClassSubjects cs
            JOIN Classes c ON cs.class_id = c.id
            JOIN Subjects s ON cs.subject_id = s.id
            JOIN AcademicYears a ON cs.academic_year_id = a.id
            JOIN Users u ON cs.teacher_id = u.id
            ORDER BY a.year_label
        """
        cur.execute(query)
        results = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in results], 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def update_class_subject_logic(class_subject_id, data):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed!"}, 500

    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE ClassSubjects
            SET class_id = %s, subject_id = %s, teacher_id = %s, academic_year_id = %s
            WHERE class_subject_id = %s
        """, (data['class_id'], data['subject_id'], data['teacher_id'], data['academic_year_id'], class_subject_id))
        conn.commit()
        return {"message": "Class Subject updated successfully!"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def delete_class_subject_logic(class_subject_id):
    conn = get_db_connection()
    if not conn:
        return {"error": "Database connection failed!"}, 500

    try:
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM ClassSubjects WHERE class_subject_id = %s", (class_subject_id,))
        conn.commit()
        return {"message": "Class Subject deleted successfully!"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()
