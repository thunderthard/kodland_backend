from flask import Blueprint, jsonify
from models.gender import Gender

genders_bp = Blueprint('genders', __name__, url_prefix='/genders')

@genders_bp.route('', methods=['GET'])
def get_genders():
    genders = Gender.query.all()

    result = [
        {
            'id_gender': gender.id_gender,
            'name': gender.name
        }
        for gender in genders
    ]

    return jsonify(result), 200