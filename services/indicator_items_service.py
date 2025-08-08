from database.database import get_db_connection


def create_indicator_item(data, tenant_id):
    indicator_id = data.get("indicator_id")
    class_id = data.get("class_id")
    description = data.get("description")
    sort_order = data.get("sort_order")

    if not all([tenant_id, indicator_id, class_id, description]):
        return None, "tenant_id, indicator_id, class_id, and description are required.", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Indicator_Items (tenant_id, indicator_id, class_id, description, sort_order)
            VALUES (%s, %s, %s, %s, %s)
        """, (tenant_id, indicator_id, class_id, description, sort_order))
        conn.commit()
        return "Indicator item created successfully.", None, 201
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def update_indicator_item(item_id, tenant_id, data):
    description = data.get("description")
    sort_order = data.get("sort_order")

    if not description:
        return None, "Description is required.", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Indicator_Items
            SET description = %s, sort_order = %s
            WHERE id = %s AND tenant_id = %s
        """, (description, sort_order, str(item_id), tenant_id))
        if cur.rowcount == 0:
            return None, "Indicator item not found or unauthorized.", 404
        conn.commit()
        return "Indicator item updated successfully.", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def delete_indicator_item(item_id, tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Indicator_Items
            WHERE id = %s AND tenant_id = %s
        """, (str(item_id), tenant_id))
        if cur.rowcount == 0:
            return None, "Indicator item not found or unauthorized.", 404
        conn.commit()
        return "Indicator item deleted successfully.", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def list_indicator_items(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, indicator_id, class_id, description, sort_order
            FROM Indicator_Items
            WHERE tenant_id = %s
            ORDER BY sort_order
        """, (tenant_id,))
        items = cur.fetchall()
        results = [{
            "id": str(row[0]),
            "indicator_id": str(row[1]),
            "class_id": str(row[2]),
            "description": row[3],
            "sort_order": row[4]
        } for row in items]
        return results, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()
