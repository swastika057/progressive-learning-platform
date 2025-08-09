from flask import jsonify
from database.database import get_db_connection


def create_billing(data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        query = """
            INSERT INTO Billing (tenant_id, student_id, bill_type_id, amount, issue_date, due_date, payment_status, payment_date, description)
            VALUES (%s, %s, %s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """
        values = (
            data['tenant_id'],
            data['student_id'],
            data['bill_type_id'],
            data['amount'],
            data.get('issue_date'),
            data.get('due_date'),
            data.get('payment_status', 'Pending'),
            data.get('payment_date'),
            data.get('description')
        )
        cur.execute(query, values)
        billing_id = cur.fetchone()[0]
        conn.commit()
        return jsonify({"message": "Billing record created", "billing_id": billing_id}), 201

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


def get_all_billing():
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("SELECT * FROM Billing")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in rows]

        return jsonify(result), 200

    except Exception as e:
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


def update_billing(billing_id, data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        update_fields = []
        values = []

        for key, value in data.items():
            update_fields.append(f"{key} = %s")
            values.append(value)

        values.append(str(billing_id))

        query = f"""
            UPDATE Billing
            SET {', '.join(update_fields)}
            WHERE id = %s
            RETURNING id;
        """

        cur.execute(query, values)
        updated_id = cur.fetchone()

        if updated_id:
            conn.commit()
            return jsonify({"message": "Billing record updated", "billing_id": updated_id[0]}), 200
        else:
            return jsonify({"error": "Billing record not found"}), 404

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()


def delete_billing(billing_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()

        cur.execute("DELETE FROM Billing WHERE id = %s RETURNING id",
                    (str(billing_id),))
        deleted = cur.fetchone()

        if deleted:
            conn.commit()
            return jsonify({"message": "Billing record deleted", "billing_id": deleted[0]}), 200
        else:
            return jsonify({"error": "Billing record not found"}), 404

    except Exception as e:
        conn.rollback()
        return jsonify({"error": str(e)}), 500

    finally:
        cur.close()
        conn.close()
