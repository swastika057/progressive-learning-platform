from flask_bcrypt import generate_password_hash
from database.database import get_db_connection
from main import app


def seed_superadmin_tenant_and_user():
    with app.app_context():
        conn = get_db_connection()
        cur = conn.cursor()

        try:
            # 1. Check if tenant already exists
            cur.execute("SELECT id FROM Tenants WHERE email = %s",
                        ('superadmin@example.com',))
            tenant = cur.fetchone()

            if tenant is None:
                # Create tenant
                cur.execute("""
                    INSERT INTO Tenants (
                        tenant_name, email, address, city, country,
                        established_date, phone, registration_number, is_active
                    ) VALUES (%s, %s, %s, %s, %s, %s, %s, %s, TRUE)
                    RETURNING id
                """, (
                    'SuperAdmin School',
                    'superadmin@example.com',
                    'Kathmandu',
                    'Kathmandu',
                    'Nepal',
                    '2020-01-01',
                    '9800000000',
                    'REG123456'
                ))

                tenant_id = cur.fetchone()[0]
                print(f" Superadmin tenant created with ID: {tenant_id}")
            else:
                tenant_id = tenant[0]
                print(
                    f"ℹ Superadmin tenant already exists with ID: {tenant_id}")

            # 2. Check if superadmin user exists
            cur.execute("SELECT id FROM Users WHERE email = %s",
                        ('admin@superadmin.com',))
            user = cur.fetchone()

            if user is None:
                password_hash = generate_password_hash(
                    'admin123').decode('utf-8')

                # Create superadmin user with tenant_id
                cur.execute("""
                    INSERT INTO Users (
                        username, password_hash, email, first_name, last_name,
                        contact_phone, gender, date_of_birth, tenant_id, is_active
                    ) VALUES (
                        %s, %s, %s, %s, %s, %s, %s, %s, %s, TRUE
                    )
                """, (
                    'superadmin',
                    password_hash,
                    'admin@superadmin.com',
                    'Super',
                    'Admin',
                    '9800000000',
                    'F',
                    '1990-01-01',
                    tenant_id
                ))

                print(" Superadmin user created.")
            else:
                print("ℹ Superadmin user already exists.")

            conn.commit()

        except Exception as e:
            conn.rollback()
            print(f" Error during seeding: {e}")
        finally:
            cur.close()
            conn.close()


if __name__ == '__main__':
    seed_superadmin_tenant_and_user()
