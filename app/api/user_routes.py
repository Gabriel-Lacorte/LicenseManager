from app.models import User, db

from flask import jsonify, request, Blueprint
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


user_routes = Blueprint('user', __name__)


# POST /api/user -> Login the user.
@user_routes.route('', methods=['POST'])
def login():
    if current_user.is_authenticated:
        return jsonify({"error": "You are already logged in."}), 403
    
    try:
        data = request.get_json()
        username = data.get('username').strip()
        password = data.get('password').strip()
    except:
        return jsonify({"error": "The input parameters were incorrect."}), 400
    
    if not username or not password:
        return jsonify({"error": "The input parameters were incorrect."}), 400
    
    user = User.query.filter_by(username=username.strip()).first()
    
    if user and user.password == password.strip():
        login_user(user)
        if user.api_key:
            return jsonify({"message": "Login successful.", "api_key": user.api_key}), 200
        
        user.api_key = User.generate_api_key()
        db.session.commit()
        return jsonify({"message": "Login successful.", "api_key": user.api_key}), 200

    return jsonify({"error": "Invalid username or password"}), 401


# POST /api/user/logout -> Logout the user.
@user_routes.route('/logout', methods=['POST'])
@User.auth_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful."})
