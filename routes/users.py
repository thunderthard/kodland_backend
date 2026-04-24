from flask import Blueprint, request, jsonify
from models import User
from db import db
from werkzeug.security import generate_password_hash
from datetime import datetime

users_bp = Blueprint('users', __name__, url_prefix='/users')

@users_bp.route('', methods=['POST'])
def create_user():
    data = request.json

    user = User(
        nickname=data.get('nickname'),
        email=data['email'],
        names=data.get('names'),
        surnames=data.get('surnames'),

        document_type_id=data.get('document_type_id'),
        number_id=data.get('number_id'),

        celphone=data.get('celphone'),
        address=data.get('address'),

        birthday=datetime.strptime(
            data['birthday'], '%Y-%m-%d'
        ).date() if data.get('birthday') else None,

        id_gender=data['id_gender'],

        zipcode=data.get('zipcode'),

        # 🔐 NUNCA guardar password en texto plano
        password=generate_password_hash(data['password']),

        startDate=datetime.utcnow(),
        id_departament=data.get('id_departament', 1)  # default
    )

    db.session.add(user)
    db.session.commit()

    return jsonify({
        'id_user': user.id_user,
        'message': 'Usuario creado correctamente'
    }), 201

