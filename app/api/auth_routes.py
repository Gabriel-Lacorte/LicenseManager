from app.models import User

from flask import jsonify, request, Blueprint
from werkzeug.security import check_password_hash
from flask_login import login_user, login_required, logout_user, current_user


auth_routes = Blueprint('auth', __name__)


# POST /api/auth/login -> Login the user.
@auth_routes.route('/login', methods=['POST'])
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
        return jsonify({"message": "Login successful."}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# POST /api/auth/logout -> Logout the user.
@auth_routes.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful."})
