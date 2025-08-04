from flask import Blueprint
from routes.login import login
from routes.users import users_bp
from routes.tenants import tenant_bp
from routes.register import register
from routes.roles import roles_bp
from routes.role_permissions import role_permissions_bp
from routes.user_roles import user_roles_bp
from routes.academic_years import academic_years
from routes.class_subject import class_sub
from routes.employees import employees_bp
from routes.classes import classes_bp
from routes.student import students_bp
from routes.subjects import subjects_bp
from routes.permissions import permissions_bp
# Central place to register all route blueprints


def register_routes(app):
    app.register_blueprint(login)
    app.register_blueprint(users_bp)
    app.register_blueprint(tenant_bp)
    app.register_blueprint(register)
    app.register_blueprint(roles_bp)
    app.register_blueprint(role_permissions_bp)
    app.register_blueprint(user_roles_bp)
    app.register_blueprint(academic_years)
    app.register_blueprint(class_sub)
    app.register_blueprint(employees_bp)
    app.register_blueprint(classes_bp)
    app.register_blueprint(students_bp)
    app.register_blueprint(subjects_bp)
    app.register_blueprint(permissions_bp)
