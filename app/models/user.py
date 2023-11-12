from .db import db

from functools import wraps
from secrets import token_hex
from flask import request, current_app
from flask_login import UserMixin, current_user, login_manager

class User(db.Model, UserMixin):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    username = db.Column(db.String(64), unique=True, nullable=False)
    password = db.Column(db.String(128), nullable=False)
    api_key = db.Column(db.String(32), nullable=True)

    def generate_api_key():
        while True:
            generated_key = token_hex(32)
            if not User.query.filter_by(api_key=generated_key).first():
                return generated_key.upper()


    def auth_required(func):
        @wraps(func)
        def decorated(*args, **kwargs):
            api_key = request.headers.get('Authorization')
            
            if current_user.is_authenticated:
                return func(*args, **kwargs)
            
            if not api_key:
                return current_app.login_manager.unauthorized()
            
            
            key = User.query.filter_by(api_key=api_key).first()
            if not key:
                return current_app.login_manager.unauthorized()

            return func(*args, **kwargs)
        
        return decorated
