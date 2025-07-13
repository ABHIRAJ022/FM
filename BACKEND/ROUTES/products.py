# server/routes/products.py
from flask import Blueprint, request, jsonify
from bson import ObjectId
import jwt
import os
from pymongo import MongoClient
from functools import wraps

products_bp = Blueprint('products', __name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()
products = db.products

# Middleware for verifying JWT
def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token is missing!'}), 403
        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            request.user = data
        except:
            return jsonify({'error': 'Token is invalid!'}), 403
        return f(*args, **kwargs)
    return decorated

@products_bp.route('/', methods=['POST'])
@token_required
def create_product():
    if request.user['role'] != 'farmer':
        return jsonify({'error': 'Access denied'}), 403

    data = request.json
    product = {
        "name": data['name'],
        "description": data['description'],
        "price": data['price'],
        "category": data['category'],
        "farmer_id": request.user['id'],
        "stock": data['stock']
    }
    result = products.insert_one(product)
    product['_id'] = str(result.inserted_id)
    return jsonify(product), 201

@products_bp.route('/', methods=['GET'])
def get_all_products():
    all_products = []
    for prod in products.find():
        prod['_id'] = str(prod['_id'])
        all_products.append(prod)
    return jsonify(all_products)

@products_bp.route('/<id>', methods=['PUT'])
@token_required
def update_product(id):
    if request.user['role'] != 'farmer':
        return jsonify({'error': 'Access denied'}), 403

    data = request.json
    update = {k: v for k, v in data.items()}
    result = products.update_one({'_id': ObjectId(id), 'farmer_id': request.user['id']}, {"$set": update})
    if result.matched_count == 0:
        return jsonify({'error': 'Not found or not allowed'}), 404
    return jsonify({'message': 'Product updated'})

@products_bp.route('/<id>', methods=['DELETE'])
@token_required
def delete_product(id):
    if request.user['role'] != 'farmer':
        return jsonify({'error': 'Access denied'}), 403

    result = products.delete_one({'_id': ObjectId(id), 'farmer_id': request.user['id']})
    if result.deleted_count == 0:
        return jsonify({'error': 'Product not found'}), 404
    return jsonify({'message': 'Product deleted'})
