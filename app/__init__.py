from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()
login_manager.login_view = "auth.login"

def create_app():
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diabetes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    db.init_app(app)
    login_manager.init_app(app)

    from .routes_auth import auth_bp
    from .routes_logs import logs_bp

    app.register_blueprint(auth_bp)
    app.register_blueprint(logs_bp)

    with app.app_context():
        from .models import User, GlucoseLog, InsulinLog  # noqa: F401
        db.create_all()

    return app
