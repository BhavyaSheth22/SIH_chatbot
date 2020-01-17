from datetime import datetime
from sih_chatbot import db, login_manager
from flask_login import UserMixin


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class User(db.Model, UserMixin):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    email = db.Column(db.String(120), unique=True, nullable=False)
    password = db.Column(db.String(60), nullable=False)
    # def __repr__(self):
    #     return f"User('{self.first_name}', '{self.email}')"

class Message(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    # username = db.Column(db.String(50))
    message = db.Column(db.String(500))
    key = db.Column(db.Boolean(), default=False) # User = true, bot = false

   
class Patient(db.Model):
    id = db.Column(db.Integer, primary_key=True)
    first_name = db.Column(db.String(30), nullable=False)
    last_name = db.Column(db.String(30), nullable=False)
    age = db.Column(db.Integer, nullable=False)
    #date of birth
    gender = db.Column(db.String(10), nullable=False)
    weight = db.Column(db.Integer, nullable=False)
    height = db.Column(db.Integer, nullable=False)
    bmi = db.Column(db.Integer, nullable=False)
    blood_group = db.Column(db.String(10), nullable=False)
    # diseases= db.Column()
