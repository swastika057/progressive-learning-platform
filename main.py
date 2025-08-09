
from flask import Flask
from extension import bcrypt
from routes import register_routes
from database.database import get_db_connection


# Add JWT config here

app = Flask(__name__)
app.secret_key = 'flash message'
# Add JWT config here

app.config['JWT_SECRET_KEY'] = 'admin@1234'  # Use a strong secret key
app.config['JWT_ALGORITHM'] = 'HS256'  # Or another algorithm if you want


bcrypt.init_app(app)

# Register all blueprints here
register_routes(app)


if __name__ == '__main__':
    app.run(debug=True)
