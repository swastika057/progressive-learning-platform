from flask import Blueprint, request, jsonify
from utils.decorators import jwt_required
from services.users_service import fetch_users, add_user, update_user, delete_user

users_bp = Blueprint('users', __name__)


@users_bp.route('/users', methods=['GET'])
@jwt_required
def get_users():
    user_claims = request.current_user_jwt_claims
    is_admin = user_claims.get('is_admin')
    tenant_id = user_claims.get('tenant_id')

    users, error = fetch_users(is_admin, tenant_id)
    if error:
        return jsonify({"error": error}), 500

    # Convert dates to ISO strings for JSON response
    user_list = []
    for user in users:
        user_list.append({
            "id": str(user["id"]),
            "username": user["username"],
            "email": user["email"],
            "first_name": user["first_name"],
            "last_name": user["last_name"],
            "contact_phone": user["contact_phone"],
            "gender": user["gender"],
            "tenant_id": str(user["tenant_id"]),
            "date_of_birth": user["date_of_birth"].isoformat() if user["date_of_birth"] else None,
            "is_active": user["is_active"],
            "last_login": user["last_login"].isoformat() if user["last_login"] else None,
            "created_at": user["created_at"].isoformat() if user["created_at"] else None,
            "updated_at": user["updated_at"].isoformat() if user["updated_at"] else None
        })
    return jsonify(users=user_list), 200


@users_bp.route('/users', methods=['POST'])
@jwt_required
def create_user():
    data = request.get_json()
    success, error = add_user(data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "User added successfully"}), 201


@users_bp.route('/users/<uuid:user_id>', methods=['PUT'])
@jwt_required
def modify_user(user_id):
    data = request.get_json()
    success, error = update_user(user_id, data)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "User updated successfully"}), 200


@users_bp.route('/users/<uuid:user_id>', methods=['DELETE'])
@jwt_required
def remove_user(user_id):
    success, error = delete_user(user_id)
    if error:
        return jsonify({"error": error}), 400
    return jsonify({"message": "User deleted successfully"}), 200
