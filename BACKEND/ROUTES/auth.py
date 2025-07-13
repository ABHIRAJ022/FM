from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from werkzeug.security import generate_password_hash, check_password_hash
import jwt
import datetime
import os

auth_bp = Blueprint('auth', __name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()
users = db.users

@auth_bp.route('/register', methods=['POST'])
def register():
    data = request.json
    if users.find_one({"email": data["email"]}):
        return jsonify({"error": "User already exists"}), 400
    
    hashed_pw = generate_password_hash(data["password"])
    user = {
        "name": data["name"],
        "email": data["email"],
        "password": hashed_pw,
        "role": data["role"]
    }
    users.insert_one(user)
    return jsonify({"message": "User registered successfully"}), 201

@auth_bp.route('/login', methods=['POST'])
def login():
    data = request.json
    user = users.find_one({"email": data["email"]})
    if not user or not check_password_hash(user["password"], data["password"]):
        return jsonify({"error": "Invalid credentials"}), 401
    
    token = jwt.encode({
        "id": str(user["_id"]),
        "role": user["role"],
        "exp": datetime.datetime.utcnow() + datetime.timedelta(days=1)
    }, os.getenv("JWT_SECRET"), algorithm="HS256")
    
    return jsonify({"token": token, "user": {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }})
