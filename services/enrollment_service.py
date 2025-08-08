from database.database import get_db_connection


def add_enrollment_record(data, tenant_id):
    student_id = data.get('student_id')
    class_id = data.get('class_id')
    academic_year_id = data.get('academic_year_id')
    enrollment_date = data.get('enrollment_date')

    if not all([student_id, class_id, academic_year_id, tenant_id]):
        return None, "Missing required fields", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Enrollments (tenant_id, student_id, class_id, academic_year_id, enrollment_date)
            VALUES (%s, %s, %s, %s, %s)
            ON CONFLICT (student_id, class_id, academic_year_id, tenant_id) DO NOTHING
        """, (tenant_id, student_id, class_id, academic_year_id, enrollment_date))
        conn.commit()
        return "Enrollment added successfully", None, 201
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def get_all_enrollments(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT
                e.id,
                e.student_id,
                u.first_name || ' ' || u.last_name AS student_name,
                c.id AS class_id,
                c.class_name,
                c.section,
                ay.id AS academic_year_id,
                ay.year_label,
                e.enrollment_date,
                e.tenant_id
            FROM Enrollments e
            JOIN Students s ON e.student_id = s.user_id
            JOIN Users u ON s.user_id = u.id
            JOIN Classes c ON e.class_id = c.id
            JOIN AcademicYears ay ON e.academic_year_id = ay.id
            WHERE e.tenant_id = %s
        """, (tenant_id,))

        rows = cur.fetchall()
        enrollments = [{
            "enrollment_id": row[0],
            "student_id": row[1],
            "student_name": row[2],
            "class_id": row[3],
            "class_name": row[4],
            "section": row[5],
            "academic_year_id": row[6],
            "academic_year": row[7],
            "enrollment_date": row[8].isoformat() if row[8] else None,
            "tenant_id": row[9]
        } for row in rows]

        return enrollments, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def update_enrollment_record(enrollment_id, tenant_id, data):
    class_id = data.get("class_id")
    academic_year_id = data.get("academic_year_id")
    enrollment_date = data.get("enrollment_date")

    if not class_id or not academic_year_id:
        return None, "Missing required fields", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Enrollments
            SET class_id = %s,
                academic_year_id = %s,
                enrollment_date = %s
            WHERE id = %s AND tenant_id = %s
        """, (class_id, academic_year_id, enrollment_date, enrollment_id, tenant_id))

        if cur.rowcount == 0:
            return None, "Enrollment not found or unauthorized", 404

        conn.commit()
        return "Enrollment updated successfully", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def delete_enrollment_record(enrollment_id, tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Enrollments
            WHERE id = %s AND tenant_id = %s
        """, (enrollment_id, tenant_id))

        if cur.rowcount == 0:
            return None, "Enrollment not found or unauthorized", 404

        conn.commit()
        return "Enrollment deleted successfully", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()
