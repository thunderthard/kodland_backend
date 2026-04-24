from flask import Blueprint, request, jsonify
from models import SystemRole
from db import db

system_roles_bp = Blueprint('system_roles', __name__, url_prefix='/system-roles')

@system_roles_bp.route('', methods=['POST'])
def create_role():
    role = SystemRole(name=request.json['name'])
    db.session.add(role)
    db.session.commit()
    return jsonify({'id_role': role.id_role}), 201