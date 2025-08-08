from database.database import get_db_connection


def add_report_card_service(data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            INSERT INTO ReportCards (
                tenant_id, student_id, academic_year_id, semester,
                issue_date, overall_comment, issued_by
            )
            VALUES (%s, %s, %s, %s, %s, %s, %s)
            RETURNING id;
        """, (
            data['tenant_id'], data['student_id'], data['academic_year_id'], data['semester'],
            data.get('issue_date'), data.get(
                'overall_comment'), data.get('issued_by')
        ))
        new_id = cur.fetchone()[0]
        conn.commit()
        return {'message': 'Report card added successfully', 'id': new_id}, 201
    except Exception as e:
        conn.rollback()
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


def get_all_report_cards_service():
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("SELECT * FROM ReportCards ORDER BY created_at DESC;")
        rows = cur.fetchall()
        columns = [desc[0] for desc in cur.description]
        result = [dict(zip(columns, row)) for row in rows]
        return result, 200
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


def get_report_card_service(report_card_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "SELECT * FROM ReportCards WHERE report_card_id = %s;", (report_card_id,))
        row = cur.fetchone()
        if row:
            columns = [desc[0] for desc in cur.description]
            return dict(zip(columns, row)), 200
        else:
            return {'error': 'Report card not found'}, 404
    except Exception as e:
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


def update_report_card_service(report_card_id, data):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute("""
            UPDATE ReportCards SET
                semester = %s,
                issue_date = %s,
                overall_comment = %s,
                issued_by = %s
            WHERE report_card_id = %s;
        """, (
            data.get('semester'), data.get(
                'issue_date'), data.get('overall_comment'),
            data.get('issued_by'), report_card_id
        ))
        conn.commit()
        if cur.rowcount == 0:
            return {'error': 'Report card not found'}, 404
        return {'message': 'Report card updated successfully'}, 200
    except Exception as e:
        conn.rollback()
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()


def delete_report_card_service(report_card_id):
    try:
        conn = get_db_connection()
        cur = conn.cursor()
        cur.execute(
            "DELETE FROM ReportCards WHERE report_card_id = %s;", (report_card_id,))
        conn.commit()
        if cur.rowcount == 0:
            return {'error': 'Report card not found'}, 404
        return {'message': 'Report card deleted successfully'}, 200
    except Exception as e:
        conn.rollback()
        return {'error': str(e)}, 500
    finally:
        cur.close()
        conn.close()
