from db import db
from datetime import datetime

class User(db.Model):
    __tablename__ = 'users'

    id_user = db.Column(db.BigInteger, primary_key=True)

    nickname = db.Column(db.String(20))
    names = db.Column(db.String(200))
    surnames = db.Column(db.String(200))

    document_type_id = db.Column(
        db.BigInteger,
        db.ForeignKey('document_types.id_document_type')
    )

    number_id = db.Column(db.BigInteger)
    celphone = db.Column(db.BigInteger)

    address = db.Column(db.String(50))
    email = db.Column(db.String(50))

    birthday = db.Column(db.Date)

    id_city = db.Column(
        db.BigInteger,
        db.ForeignKey('cities.id_city')
    )

    id_neighborhood = db.Column(db.BigInteger)

    id_gender = db.Column(
        db.Integer,
        db.ForeignKey('genders.id_gender'),
        nullable=False
    )

    password = db.Column(db.String(20))  # ⚠️ luego hash, no plaintext

    zipcode = db.Column(db.String(20))

    startDate = db.Column(
        'startDate',
        db.DateTime(timezone=True)
    )

    lastConnection = db.Column(
        'lastConnection',
        db.DateTime(timezone=True)
    )

    id_departament = db.Column(db.Integer, nullable=False)

    # ==========================
    # 🔗 RELACIONES
    # ==========================

    gender = db.relationship('Gender', backref='users')
    city = db.relationship('City', backref='users')
    document_type = db.relationship('DocumentType', backref='users')

    # Estas relaciones ya existen por backref
    # goals_scored
    # goals_reported
    # matches_created
    # match_confirmations


class SystemRole(db.Model):
    __tablename__ = 'system_roles'

    id_role = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class UserSystemRole(db.Model):
    __tablename__ = 'user_system_roles'

    id_user = db.Column(db.BigInteger, db.ForeignKey('users.id_user'), primary_key=True)
    id_role = db.Column(db.BigInteger, db.ForeignKey('system_roles.id_role'), primary_key=True)
    assigned_at = db.Column(db.DateTime, default=datetime.utcnow)


class Position(db.Model):
    __tablename__ = 'positions'

    id_position = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), unique=True, nullable=False)


class Team(db.Model):
    __tablename__ = 'teams'

    id_team = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False)
    created_at = db.Column(db.DateTime, default=datetime.utcnow)


class TeamMember(db.Model):
    __tablename__ = 'team_members'

    id_team_member = db.Column(db.BigInteger, primary_key=True)
    id_user = db.Column(db.BigInteger, db.ForeignKey('users.id_user'))
    id_team = db.Column(db.BigInteger, db.ForeignKey('teams.id_team'))
    id_position = db.Column(db.BigInteger, db.ForeignKey('positions.id_position'))
    jersey_number = db.Column(db.Integer)
    is_admin = db.Column(db.Boolean, default=False)
    active = db.Column(db.Boolean, default=True)

    __table_args__ = (
        db.UniqueConstraint('id_user', 'id_team'),
    )

class Gender(db.Model):
    __tablename__ = 'genders'

    id_gender = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class DocumentType(db.Model):
    __tablename__ = 'document_types'

    id_document_type = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(50), nullable=False, unique=True)

class City(db.Model):
    __tablename__ = 'cities'

    id_city = db.Column(db.BigInteger, primary_key=True)
    name = db.Column(db.String(100), nullable=False, unique=True)
class Goal(db.Model):
    __tablename__ = 'goals'

    id_goal = db.Column(db.BigInteger, primary_key=True)
    
    match_id = db.Column(
        db.BigInteger,
        db.ForeignKey('matches.id_match'),
        nullable=False
    )

    team_id = db.Column(
        db.BigInteger,
        db.ForeignKey('teams.id_team'),
        nullable=False
    )

    player_id = db.Column(
        db.BigInteger,
        db.ForeignKey('users.id_user'),
        nullable=False
    )

    minute = db.Column(db.Integer, nullable=False)

    reported_by = db.Column(
        db.BigInteger,
        db.ForeignKey('users.id_user'),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now()
    )

    # 🔗 RELACIONES
    scorer = db.relationship(
        'User',
        foreign_keys=[player_id],
        backref='goals_scored'
    )

    reporter = db.relationship(
        'User',
        foreign_keys=[reported_by],
        backref='goals_reported'
    )

class Match(db.Model):
    __tablename__ = 'matches'

    id_match = db.Column(db.BigInteger, primary_key=True)

    home_team_id = db.Column(db.BigInteger, nullable=False)
    away_team_id = db.Column(db.BigInteger, nullable=False)

    match_date = db.Column(db.DateTime(timezone=True), nullable=False)
    location = db.Column(db.String(100))

    status = db.Column(
        db.String(20),
        default='SCHEDULED'
    )  # SCHEDULED | IN_PROGRESS | FINISHED

    created_by = db.Column(
        db.BigInteger,
        db.ForeignKey('users.id_user'),
        nullable=False
    )

    created_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now()
    )

    # 🔗 RELACIONES
    creator = db.relationship(
        'User',
        backref='matches_created'
    )

    goals = db.relationship(
        'Goal',
        backref='match',
        cascade='all, delete-orphan'
    )

class MatchConfirmation(db.Model):
    __tablename__ = 'match_confirmations'

    id_confirmation = db.Column(db.BigInteger, primary_key=True)

    match_id = db.Column(
        db.BigInteger,
        db.ForeignKey('matches.id_match'),
        nullable=False
    )

    confirmed_by = db.Column(
        db.BigInteger,
        db.ForeignKey('users.id_user'),
        nullable=False
    )

    confirmed_at = db.Column(
        db.DateTime(timezone=True),
        server_default=db.func.now()
    )

    # 🔗 RELACIONES
    user = db.relationship(
        'User',
        backref='match_confirmations'
    )

    match = db.relationship(
        'Match',
        backref='confirmations'
    )

class Locality(db.Model):
    __tablename__ = 'localities'

    id_locality = db.Column(db.BigInteger, primary_key=True)

    name = db.Column(db.String)

    id_city = db.Column(
        db.BigInteger,
        db.ForeignKey('cities.id_city')
    )

    # 🔗 RELACIONES
    city = db.relationship(
        'City',
        backref='localities'
    )