from flask import Blueprint, request, redirect, url_for, session, jsonify
from .db.crud import add_login, validate_login


auth = Blueprint('auth', __name__)


@auth.route('/clear-session', methods=['GET'])
def clear_session():
    session.clear()  # Clear the session
    return redirect(url_for('auth.login'))


@auth.route("/login", methods=["POST"])
def login():
    data = request.get_json()
    username = data.get('username')
    password = data.get('password')
    
    if validate_login(username, password):
        session["username"] = username
        if username == "admin":
            session["is_admin"] = True
            
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 401
    
    
@auth.route("/register", methods=["POST"])
def register():
    data = request.get_json()
    username = data.get("username")
    password = data.get("password")
    
    if add_login(username, password):
        return jsonify({"success": True}), 200
    else:
        return jsonify({"success": False}), 401

