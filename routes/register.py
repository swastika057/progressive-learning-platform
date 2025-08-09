from flask import Blueprint, request, jsonify
from utils.decorators import admin_required
from services.register_service import register_tenant

register = Blueprint('register', __name__)


@register.route('/tenants/register', methods=['POST'])
@admin_required
def register_tenants():
    data = request.get_json()
    if not data:
        return jsonify({"error": "Missing or invalid JSON"}), 400

    # Call service function to handle registration logic
    response, status = register_tenant(data)
    return jsonify(response), status
