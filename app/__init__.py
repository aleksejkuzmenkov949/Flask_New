from flask import Flask
from flask_migrate import Migrate
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from app.models import db, User
from app.config import Config
from app.routers.users import users_bp
from app.routers.notes import notes_bp

db = SQLAlchemy()
migrate = Migrate()
login_manager = LoginManager()


def create_app():
    app = Flask(__name__)
    app.config.from_object(Config)
    db.init_app(app)
    migrate.init_app(app, db)
    login_manager.init_app(app)

    app.register_blueprint(users_bp, url_prefix='/users')
    app.register_blueprint(notes_bp, url_prefix='/notes')

    return app


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
