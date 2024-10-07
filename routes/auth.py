from flask import Blueprint, request, jsonify
import bcrypt
from models import User
from utils.token import generate_token, decode_token

auth_bp = Blueprint('auth', __name__)

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    username = data['username']
    password = data['password']

    # Check if user already exists
    if User.find_by_username(username):
        return jsonify({"message": "User already exists"}), 400

    hashed_password = bcrypt.hashpw(password.encode('utf-8'), bcrypt.gensalt())
    User.insert_user(username, hashed_password.decode('utf-8'))

    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    username = data['username']
    password = data['password']

    user = User.find_by_username(username)
    if user and bcrypt.checkpw(password.encode('utf-8'), user['password'].encode('utf-8')):
        token = generate_token(user['_id'])
        return jsonify({"token": token}), 200

    return jsonify({"message": "Invalid credentials"}), 401
