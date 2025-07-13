# server/utils/jwt_utils.py

import jwt
import os
from functools import wraps
from flask import request, jsonify

SECRET = os.getenv("JWT_SECRET")

def token_required(role=None):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            token = request.headers.get("Authorization")
            if not token:
                return jsonify({"error": "Missing token"}), 403
            try:
                decoded = jwt.decode(token, SECRET, algorithms=["HS256"])
                request.user = decoded
                if role and decoded.get("role") != role:
                    return jsonify({"error": "Unauthorized"}), 403
            except jwt.ExpiredSignatureError:
                return jsonify({"error": "Token expired"}), 403
            except jwt.InvalidTokenError:
                return jsonify({"error": "Invalid token"}), 403
            return f(*args, **kwargs)
        return wrapper
    return decorator
