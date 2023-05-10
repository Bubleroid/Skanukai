from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin
from app.config import db

class User(UserMixin, db.Model):
    __tablename__ = 'Users'
    id = db.Column(db.Integer, primary_key = True)
    username = db.Column(db.String(120), unique = True)
    email = db.Column(db.String(60), unique = True, index=True)
    cart = db.Column(db.String, default='[]')
    password_hash = db.Column(db.String(120))
    admin = db.Column(db.Boolean, default=False)
    
    def __repr__(self) -> str:
        return '<User {}'.format(self.username)
    def set_password(self, password):
        self.password_hash = generate_password_hash(password)
    def check_password(self, password):
        return check_password_hash(self.password_hash, password)

class Treat(db.Model):
    __tablename__ = 'Treat'
    id = db.Column(db.Integer, primary_key = True)
    name = db.Column(db.String(45), unique=True)
    descreption = db.Column(db.String(120))
    price = db.Column(db.Float)
    count = db.Column(db.Integer)
    image = db.Column(db.String)

    def __repr__(self) -> str:
        return f'name: {self.name}, price: {self.price}'

