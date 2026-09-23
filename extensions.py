"""
NutriSnap-X - Flask Extensions
Initialize extensions separately to avoid circular imports
"""

from flask_sqlalchemy import SQLAlchemy
from flask_login import LoginManager

db = SQLAlchemy()
login_manager = LoginManager()
