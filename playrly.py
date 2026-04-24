from flask import Flask
from db import db
from flask_migrate import Migrate
from dotenv import load_dotenv
import os

load_dotenv()

def create_app():
    app=Flask(__name__,static_url_path='')

    app.config['SQLALCHEMY_DATABASE_URI'] = os.getenv("DATABASE_URL")
    app.config['SQLALCHEMY_TRACK_MODIFICATIONS'] = False

    db.init_app(app)
    migrate = Migrate(app, db)

    from routes.users import users_bp
    from routes.positions import positions_bp
    from routes.system_roles import system_roles_bp
    from routes.teams import teams_bp
    from routes.team_members import team_members_bp

    app.register_blueprint(users_bp)
    app.register_blueprint(positions_bp)
    app.register_blueprint(system_roles_bp)
    app.register_blueprint(teams_bp)
    app.register_blueprint(team_members_bp)

    @app.route('/',methods=["GET"])
    def root():
        return app.send_static_file('index.html')

    return app

app = create_app()

if __name__ == "__main__":
    app.run(debug=True)