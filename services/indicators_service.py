from database.database import get_db_connection


def create_indicator(data, tenant_id):
    subject_id = data.get("subject_id")
    name = data.get("name")
    sort_order = data.get("sort_order")

    if not tenant_id or not subject_id or not name:
        return None, "tenant_id, subject_id, and name are required.", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Indicators (tenant_id, subject_id, name, sort_order)
            VALUES (%s, %s, %s, %s)
        """, (tenant_id, subject_id, name, sort_order))
        conn.commit()
        return "Indicator created successfully.", None, 201
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def get_indicators(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT * FROM Indicators WHERE tenant_id = %s
        """, (tenant_id,))
        indicators = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        results = [dict(zip(columns, row)) for row in indicators]
        return results, None
    except Exception as e:
        return None, str(e)
    finally:
        cur.close()
        conn.close()


def update_indicator(indicator_id, tenant_id, data):
    subject_id = data.get("subject_id")
    name = data.get("name")
    sort_order = data.get("sort_order")

    if not tenant_id or not subject_id or not name:
        return None, "tenant_id, subject_id, and name are required.", 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Indicators SET subject_id = %s, name = %s, sort_order = %s
            WHERE id = %s AND tenant_id = %s
        """, (subject_id, name, sort_order, indicator_id, tenant_id))
        if cur.rowcount == 0:
            return None, "Indicator not found or unauthorized", 404
        conn.commit()
        return "Indicator updated successfully.", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()


def delete_indicator(indicator_id, tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Indicators WHERE id = %s AND tenant_id = %s
        """, (indicator_id, tenant_id))
        if cur.rowcount == 0:
            return None, "Indicator not found or unauthorized", 404
        conn.commit()
        return "Indicator deleted successfully.", None, 200
    except Exception as e:
        conn.rollback()
        return None, str(e), 500
    finally:
        cur.close()
        conn.close()
