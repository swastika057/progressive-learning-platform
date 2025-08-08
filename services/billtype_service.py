# services/billtypes_service.py

from database.database import get_db_connection


def add_bill_type_service(tenant_id, bill_type_name, description):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO BillTypes (tenant_id, bill_type_name, description)
            VALUES (%s, %s, %s)
            RETURNING id
        """, (tenant_id, bill_type_name, description))
        bill_type_id = cur.fetchone()[0]
        conn.commit()
        return {"message": "Bill type added successfully", "id": bill_type_id}, 201
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def get_bill_types_service(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, bill_type_name, description
            FROM BillTypes
            WHERE tenant_id = %s
        """, (tenant_id,))
        billtypes = cur.fetchall()

        result = [
            {"id": bt[0],
                "bill_type_name": bt[1], "description": bt[2]}
            for bt in billtypes
        ]
        return result, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def update_bill_type_service(bill_type_id, bill_type_name, description):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE BillTypes
            SET bill_type_name = %s, description = %s
            WHERE bill_type_id = %s
        """, (bill_type_name, description, bill_type_id))
        conn.commit()
        return {"message": "Bill type updated successfully"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def delete_bill_type_service(bill_type_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("DELETE FROM BillTypes WHERE bill_type_id = %s",
                    (bill_type_id,))
        conn.commit()
        return {"message": "Bill type deleted successfully"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()
