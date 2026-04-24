from flask import Blueprint, request, jsonify
from models import TeamMember
from db import db

team_members_bp = Blueprint('team_members', __name__, url_prefix='/team-members')

@team_members_bp.route('', methods=['POST'])
def add_player():
    data = request.json

    member = TeamMember(
        id_user=data['id_user'],
        id_team=data['id_team'],
        id_position=data['id_position'],
        jersey_number=data.get('jersey_number'),
        is_admin=data.get('is_admin', False)
    )

    db.session.add(member)
    db.session.commit()

    return jsonify({'id_team_member': member.id_team_member}), 201