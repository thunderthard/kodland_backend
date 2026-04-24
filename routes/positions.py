from flask import Blueprint, request, jsonify
from models import Position
from db import db

positions_bp = Blueprint('positions', __name__, url_prefix='/positions')

@positions_bp.route('', methods=['POST'])
def create_position():
    position = Position(name=request.json['name'])
    db.session.add(position)
    db.session.commit()
    return jsonify({'id_position': position.id_position}), 201