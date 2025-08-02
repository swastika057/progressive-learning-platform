from flask import Blueprint
from routes.login import login
from routes.users import users
from routes.tenants import tenant_bp
from routes.register import register
from routes.roles import roles_bp
from routes.role_permissions import roles_permission
from routes.user_roles import user_roles

# Central place to register all route blueprints


def register_routes(app):
    app.register_blueprint(login)
    app.register_blueprint(users)
    app.register_blueprint(tenant_bp)
    app.register_blueprint(register)
    app.register_blueprint(roles_bp)
    app.register_blueprint(roles_permission)
    app.register_blueprint(user_roles)
