from flask import Blueprint, request, jsonify
from models import Team
from db import db

teams_bp = Blueprint('teams', __name__, url_prefix='/teams')

@teams_bp.route('', methods=['POST'])
def create_team():
    team = Team(name=request.json['name'])
    db.session.add(team)
    db.session.commit()
    return jsonify({'id_team': team.id_team}), 201