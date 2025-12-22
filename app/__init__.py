# app/__init__.py
from flask import Flask
from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager
import os

db = SQLAlchemy()
login_manager = LoginManager()

def create_app(test_config: dict | None = None):
    app = Flask(__name__)
    app.config["SECRET_KEY"] = os.environ.get("SECRET_KEY", "dev-secret-key")
    app.config["SQLALCHEMY_DATABASE_URI"] = "sqlite:///diabetes.db"
    app.config["SQLALCHEMY_TRACK_MODIFICATIONS"] = False

    # ✅ allow tests to override config (DB, TESTING, etc.)
    if test_config:
        app.config.update(test_config)

    db.init_app(app)
    login_manager.init_app(app)
    login_manager.login_view = None  # demo-friendly :contentReference[oaicite:4]{index=4}

    from .routes_auth import auth_bp
    from .routes_logs import logs_bp
    app.register_blueprint(auth_bp)
    app.register_blueprint(logs_bp)

    with app.app_context():
        from .models import User, GlucoseLog, InsulinLog  # noqa: F401
        db.create_all()

    return app
