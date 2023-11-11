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
        return jsonify({"message": "Login successful."}), 200
    else:
        return jsonify({"error": "Invalid username or password"}), 401


# PUT /api/user -> Change the user's password.
@user_routes.route('', methods=['PUT'])
@login_required
def change_password():
    try:
        data = request.get_json()
        old_password = data.get('old_password').strip()
        new_password = data.get('new_password').strip()
    except:
        return jsonify({"error": "The input parameters were incorrect."}), 400
    
    if not old_password or not new_password:
        return jsonify({"error": "The input parameters were incorrect."}), 400
    
    if len(new_password) > 100:
        return jsonify({"error": "The password cannot be more than 100 characters."}), 400
    
    if not check_password_hash(current_user.password, old_password):
        return jsonify({"error": "The old password is incorrect."}), 400
    
    current_user.password = new_password
    db.session.commit()
    
    return jsonify({"message": "Password changed successfully."}), 200

# POST /api/user/logout -> Logout the user.
@user_routes.route('/logout', methods=['POST'])
@login_required
def logout():
    logout_user()
    return jsonify({"message": "Logout successful."})
