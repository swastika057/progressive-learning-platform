from flask_bcrypt import generate_password_hash
from database.database import get_db_connection  # adjust import if needed
from main import app


def seed_superadmin_tenant():
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # Check if the tenant superadmin already exists
            cur.execute("SELECT id FROM Tenants WHERE email = %s",
                        ('superadmin@example.com',))
            tenant = cur.fetchone()

            if tenant is None:
                password_hash = generate_password_hash(
                    'superadmin123').decode('utf-8')

                cur.execute("""
                    INSERT INTO Tenants (
                        tenant_name, email, password_hash, address, city, country, 
                        established_date, phone, registration_number, is_active
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s,
                        %s, %s, %s, TRUE
                    )
                    RETURNING id
                """, (
                    'SaaS Admin',
                    'superadmin@example.com',
                    password_hash,
                    'Kathmandu',
                    'Kathmandu',
                    'Nepal',
                    '2020-01-01',
                    '9800000000',
                    'REG123456'
                ))

                tenant_id = cur.fetchone()[0]
                print(f"Superadmin tenant created with ID: {tenant_id}")
            else:
                print("Superadmin tenant already exists.")

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f"Error seeding superadmin tenant: {e}")
        finally:
            cur.close()
            conn.close()


if __name__ == '__main__':
    seed_superadmin_tenant()
