import jwt
from datetime import datetime, timedelta, timezone
from flask import current_app


def create_jwt_token(user_id, username, is_admin=False, tenant_id=None, email=None, roles=None):
    roles = roles or []
    payload = {
        "exp": datetime.now(timezone.utc) + timedelta(minutes=60),
        "iat": datetime.now(timezone.utc),
        "sub": user_id,
        "username": username,
        "is_admin": is_admin,
        "tenant_id": tenant_id,
        "email": email,
        "roles": roles
    }
    return jwt.encode(payload, current_app.config['JWT_SECRET_KEY'], algorithm=current_app.config['JWT_ALGORITHM'])


def decode_jwt_token(token):
    try:
        return jwt.decode(token, current_app.config['JWT_SECRET_KEY'], algorithms=[current_app.config['JWT_ALGORITHM']])
    except jwt.ExpiredSignatureError:
        return None
    except jwt.InvalidTokenError:
        return None
