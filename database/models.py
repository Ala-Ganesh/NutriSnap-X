"""
NutriSnap-X - Database Models
SQLAlchemy ORM models for all entities
"""

from datetime import datetime
from flask_login import UserMixin
from extensions import db


class User(UserMixin, db.Model):
    """Application user"""
    __tablename__ = 'users'

    id                 = db.Column(db.Integer, primary_key=True)
    full_name          = db.Column(db.String(120), nullable=False)
    email              = db.Column(db.String(180), unique=True, nullable=False, index=True)
    password_hash      = db.Column(db.String(256), nullable=False)
    daily_calorie_goal = db.Column(db.Integer, default=2000)
    protein_goal       = db.Column(db.Integer, default=60)
    fibre_goal         = db.Column(db.Integer, default=30)
    created_at         = db.Column(db.DateTime, default=datetime.utcnow)

    food_logs    = db.relationship('FoodLog',    backref='user', lazy=True, cascade='all, delete-orphan')
    barcode_logs = db.relationship('BarcodeLog', backref='user', lazy=True, cascade='all, delete-orphan')

    def __repr__(self):
        return f'<User {self.email}>'


class FoodLog(db.Model):
    """Food consumption log entry"""
    __tablename__ = 'food_logs'

    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False, index=True)
    food_name = db.Column(db.String(200), nullable=False)
    calories  = db.Column(db.Float, default=0.0)
    protein   = db.Column(db.Float, default=0.0)
    carbs     = db.Column(db.Float, default=0.0)
    fat       = db.Column(db.Float, default=0.0)
    fibre     = db.Column(db.Float, default=0.0)
    source    = db.Column(db.String(50), default='manual')   # image | barcode | manual
    image_url = db.Column(db.String(500), nullable=True)
    logged_at = db.Column(db.DateTime, default=datetime.utcnow, index=True)

    def to_dict(self):
        return {
            'id'       : self.id,
            'food_name': self.food_name,
            'calories' : self.calories,
            'protein'  : self.protein,
            'carbs'    : self.carbs,
            'fat'      : self.fat,
            'fibre'    : self.fibre,
            'source'   : self.source,
            'logged_at': self.logged_at.strftime('%Y-%m-%d %H:%M')
        }

    def __repr__(self):
        return f'<FoodLog {self.food_name} {self.calories}kcal>'


class BarcodeLog(db.Model):
    """Barcode scan log"""
    __tablename__ = 'barcode_logs'

    id        = db.Column(db.Integer, primary_key=True)
    user_id   = db.Column(db.Integer, db.ForeignKey('users.id'), nullable=False)
    barcode   = db.Column(db.String(50), nullable=False)
    food_name = db.Column(db.String(200))
    brand     = db.Column(db.String(200))
    calories  = db.Column(db.Float, default=0.0)
    protein   = db.Column(db.Float, default=0.0)
    carbs     = db.Column(db.Float, default=0.0)
    fat       = db.Column(db.Float, default=0.0)
    fibre     = db.Column(db.Float, default=0.0)
    source    = db.Column(db.String(50), default='barcode')
    scanned_at = db.Column(db.DateTime, default=datetime.utcnow)

    def __repr__(self):
        return f'<BarcodeLog {self.barcode} {self.food_name}>'
