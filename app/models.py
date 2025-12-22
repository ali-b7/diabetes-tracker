from datetime import datetime

from flask_login import UserMixin
from werkzeug.security import generate_password_hash, check_password_hash
from app import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(255), unique=True, nullable=False)
    password_hash = db.Column(db.String(255), nullable=False)

    def set_password(self, password: str) -> None:
        self.password_hash = generate_password_hash(password)

    def check_password(self, password: str) -> bool:
        return check_password_hash(self.password_hash, password)


@login_manager.user_loader
def load_user(user_id):
    return db.session.get(User, int(user_id))


class GlucoseLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    value = db.Column(db.Float, nullable=False)
    unit = db.Column(db.String(10), nullable=False, default="mg/dL")
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(500))


class InsulinLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"), nullable=True)

    insulin_type = db.Column(db.String(50), nullable=False)
    units = db.Column(db.Float, nullable=False)
    recorded_at = db.Column(db.DateTime, nullable=False, default=datetime.utcnow)
    notes = db.Column(db.String(500))
