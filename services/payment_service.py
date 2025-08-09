from database.database import get_db_connection
from psycopg2.extras import RealDictCursor
from datetime import datetime


def create_payment(data):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
        INSERT INTO Payments (tenant_id, bill_id, amount_paid, payment_date, payment_method, transaction_id)
        VALUES (%s, %s, %s, %s, %s, %s)
        RETURNING *;
        """, (
            data['tenant_id'],
            data['bill_id'],
            data['amount_paid'],
            data.get('payment_date', datetime.today().date()),
            data['payment_method'],
            data['transaction_id']
        ))
        payment = cur.fetchone()
        conn.commit()
        return payment
    finally:
        cur.close()
        conn.close()


def get_payments(tenant_id, bill_id):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        cur.execute("""
            SELECT * FROM Payments
            WHERE tenant_id = %s AND bill_id = %s
        """, (tenant_id, bill_id))
        payments = cur.fetchall()
        return payments
    finally:
        cur.close()
        conn.close()


def update_payment(payment_id, data):
    conn = get_db_connection()
    cur = conn.cursor(cursor_factory=RealDictCursor)
    try:
        query = """
        UPDATE Payments
        SET amount_paid = %s,
            payment_date = %s,
            payment_method = %s,
            transaction_id = %s
        WHERE payment_id = %s
        RETURNING *;
        """
        cur.execute(query, (
            data['amount_paid'],
            data.get('payment_date', datetime.today().date()),
            data['payment_method'],
            data['transaction_id'],
            payment_id
        ))
        updated_payment = cur.fetchone()
        conn.commit()
        return updated_payment
    finally:
        cur.close()
        conn.close()


def delete_payment(payment_id):
    conn = get_db_connection()
    cur = conn.cursor()
    try:
        cur.execute("DELETE FROM Payments WHERE payment_id = %s;",
                    (payment_id,))
        deleted_count = cur.rowcount
        conn.commit()
        return deleted_count
    finally:
        cur.close()
        conn.close()
