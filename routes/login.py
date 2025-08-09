from flask import Blueprint, request, jsonify
from utils.jwt_handler import create_jwt_token
from services.login_service import authenticate_user

login = Blueprint('login', __name__)


@login.route('/users/login', methods=['POST'])
def user_login():
    data = request.get_json()
    email = data.get('email')
    password = data.get('password')

    user_data, error = authenticate_user(email, password)
    if error:
        # If error is due to missing fields or auth fail, use 400 or 401 appropriately
        if error == "Email and password are required":
            return jsonify({"msg": error}), 400
        elif error == "Invalid email or password":
            return jsonify({"msg": error}), 401
        else:
            return jsonify({"msg": f"Login failed: {error}"}), 500

    token = create_jwt_token(
        user_id=user_data['user_id'],
        username=user_data['username'],
        email=user_data['email'],
        tenant_id=user_data['tenant_id'],
        roles=user_data['roles']
    )
    return jsonify(access_token=token), 200
