from functools import wraps
from flask import request, jsonify, redirect, url_for, flash
from utils.jwt_handler import decode_jwt_token


def jwt_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        token = request.cookies.get(
            'jwt_token') or request.headers.get('Authorization')
        if not token:
            return jsonify({"error": "Authentication required."}), 401
        if token.startswith("Bearer "):
            token = token[7:]
        payload = decode_jwt_token(token)
        if not payload:
            return jsonify({"error": "Invalid or expired token."}), 401
        request.current_user_jwt_claims = payload
        return f(*args, **kwargs)
    return decorated_function


def admin_required(f):
    @wraps(f)
    def decorated_function(*args, **kwargs):
        user = getattr(request, 'current_user_jwt_claims', None)
        if not user or not user.get('is_admin'):
            return jsonify({"error": "Admin access only."}), 403
        return f(*args, **kwargs)
    return decorated_function
