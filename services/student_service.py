# services/student_service.py
from database.database import get_db_connection


def add_student(user_id, tenant_id, roll_no, dob, address, parent_name, parent_contact, enrollment_date):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Students (user_id, tenant_id, roll_no, date_of_birth, address, parent_name, parent_contact, enrollment_date)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s)
        """, (user_id, tenant_id, roll_no, dob, address, parent_name, parent_contact, enrollment_date))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def get_students():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Students")
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in rows]
    finally:
        cur.close()
        conn.close()


def update_student(user_id, tenant_id, roll_no, dob, address, parent_name, parent_contact, enrollment_date):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Students SET
            roll_no = COALESCE(%s, roll_no),
            date_of_birth = COALESCE(%s, date_of_birth),
            address = COALESCE(%s, address),
            parent_name = COALESCE(%s, parent_name),
            parent_contact = COALESCE(%s, parent_contact),
            enrollment_date = COALESCE(%s, enrollment_date)
            WHERE user_id = %s AND tenant_id = %s
        """, (roll_no, dob, address, parent_name, parent_contact, enrollment_date, str(user_id), str(tenant_id)))
        updated = cur.rowcount
        conn.commit()
        return updated
    finally:
        cur.close()
        conn.close()


def delete_student(user_id, tenant_id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Students WHERE user_id = %s AND tenant_id = %s", (str(
            user_id), str(tenant_id)))
        deleted = cur.rowcount
        conn.commit()
        return deleted
    finally:
        cur.close()
        conn.close()
