# services/employee_service.py
from database.database import get_db_connection


def get_all_employees():
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("SELECT * FROM Employees")
        rows = cur.fetchall()
        cols = [desc[0] for desc in cur.description]
        return [dict(zip(cols, row)) for row in rows]
    finally:
        cur.close()
        conn.close()


def create_employee(user_id, tenant_id, department, hire_date, qualifications):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Employees (user_id, tenant_id, department, hire_date, qualifications)
            VALUES (%s, %s, %s, %s, %s)
        """, (user_id, tenant_id, department, hire_date, qualifications))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def update_employee(id, user_id, tenant_id, department, hire_date, qualifications):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("""
            UPDATE Employees
            SET user_id = %s, tenant_id = %s, department = %s,
                hire_date = %s, qualifications = %s
            WHERE id = %s
        """, (user_id, tenant_id, department, hire_date, qualifications, id))
        conn.commit()
    finally:
        cur.close()
        conn.close()


def delete_employee(id):
    conn = get_db_connection()
    try:
        cur = conn.cursor()
        cur.execute("DELETE FROM Employees WHERE id = %s", (id,))
        conn.commit()
        return cur.rowcount
    finally:
        cur.close()
        conn.close()
