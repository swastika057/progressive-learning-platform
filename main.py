
from flask import Flask
from extension import bcrypt
from routes import register_routes
from database.database import get_db_connection

app = Flask(__name__)
app.secret_key = 'flash message'

bcrypt.init_app(app)

# Register all blueprints here
register_routes(app)


if __name__ == '__main__':
    app.run(debug=True)
