from flask import Blueprint
from routes.login import login
from routes.users import users_bp
from routes.tenants import tenant_bp
from routes.register import register
from routes.roles import roles_bp
from routes.role_permissions import roles_permission
from routes.user_roles import user_roles
from routes.academic_years import academic_years
from routes.class_subject import class_sub
from routes.employees import employees_bp
from routes.classes import classes
from routes.student import student
from routes.subjects import subjects_bp
from routes.permissions import permissions_bp
# Central place to register all route blueprints


def register_routes(app):
    app.register_blueprint(login)
    app.register_blueprint(users_bp)
    app.register_blueprint(tenant_bp)
    app.register_blueprint(register)
    app.register_blueprint(roles_bp)
    app.register_blueprint(roles_permission)
    app.register_blueprint(user_roles)
    app.register_blueprint(academic_years)
    app.register_blueprint(class_sub)
    app.register_blueprint(employees_bp)
    app.register_blueprint(classes)
    app.register_blueprint(student)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(permissions_bp)
