# services/milestones_service.py

from database.database import get_db_connection


def create_milestone_service(tenant_id, milestone, description):
    if milestone not in ('A', 'B', 'C', 'D'):
        return {"error": "Milestone must be one of A, B, C, D"}, 400

    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO Milestones (tenant_id, milestone, description)
            VALUES (%s, %s, %s)
        """, (tenant_id, milestone, description))
        conn.commit()
        return {"message": "Milestone created"}, 201
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def get_milestones_service(tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            SELECT id, milestone, description
            FROM Milestones
            WHERE tenant_id = %s
        """, (tenant_id,))
        rows = cur.fetchall()
        milestones = [{"id": r[0], "milestone": r[1],
                       "description": r[2]} for r in rows]
        return milestones, 200
    except Exception as e:
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def update_milestone_service(milestone_id, tenant_id, description):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE Milestones SET description = %s
            WHERE id = %s AND tenant_id = %s
        """, (description, milestone_id, str(tenant_id)))
        if cur.rowcount == 0:
            return {"error": "Milestone not found"}, 404
        conn.commit()
        return {"message": "Milestone updated"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()


def delete_milestone_service(milestone_id, tenant_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            DELETE FROM Milestones
            WHERE id = %s AND tenant_id = %s
        """, (milestone_id, str(tenant_id)))
        if cur.rowcount == 0:
            return {"error": "Milestone not found"}, 404
        conn.commit()
        return {"message": "Milestone deleted"}, 200
    except Exception as e:
        conn.rollback()
        return {"error": str(e)}, 500
    finally:
        cur.close()
        conn.close()
