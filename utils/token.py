import jwt
from flask import request, jsonify
from functools import wraps
from config import Config
from models import User

def generate_token(user_id):
    payload = {"user_id": str(user_id)}
    return jwt.encode(payload, Config.SECRET_KEY, algorithm="HS256")

def decode_token(token):
    try:
        payload = jwt.decode(token, Config.SECRET_KEY, algorithms=["HS256"])
        return payload['user_id']
    except jwt.ExpiredSignatureError:
        return None

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({"message": "Token is missing!"}), 403
        
        user_id = decode_token(token)
        if not user_id:
            return jsonify({"message": "Token is invalid!"}), 403
        
        current_user = User.find_by_id(user_id)
        return f(current_user, *args, **kwargs)
    
    return decorated
