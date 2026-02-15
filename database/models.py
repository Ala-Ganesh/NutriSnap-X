from flask_login import UserMixin
from extensions import db, login_manager


class User(UserMixin, db.Model):
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(100))
    email = db.Column(db.String(120), unique=True)
    password = db.Column(db.String(200))

    age = db.Column(db.Integer)
    weight = db.Column(db.Float)
    height = db.Column(db.Float)
    goal = db.Column(db.String(50))   # weight_loss / muscle_gain / maintain

class MealLog(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    user_id = db.Column(db.Integer, db.ForeignKey("user.id"))

    food = db.Column(db.String(100))
    calories = db.Column(db.Float)
    protein = db.Column(db.Float)
    carbs = db.Column(db.Float)

    image = db.Column(db.String(200))
    timestamp = db.Column(db.DateTime, default=db.func.now())



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))
