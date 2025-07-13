# server/routes/orders.py
from flask import Blueprint, request, jsonify
from pymongo import MongoClient
from bson import ObjectId
import jwt
import os
import datetime
from functools import wraps

orders_bp = Blueprint('orders', __name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()
orders = db.orders
products = db.products

def token_required(f):
    @wraps(f)
    def decorated(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 403
        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            request.user = data
        except:
            return jsonify({'error': 'Invalid token'}), 403
        return f(*args, **kwargs)
    return decorated

@orders_bp.route('/', methods=['POST'])
@token_required
def place_order():
    if request.user['role'] != 'buyer':
        return jsonify({'error': 'Access denied'}), 403

    data = request.json
    order = {
        "buyer_id": request.user['id'],
        "products": data['products'],  # list of {product_id, qty}
        "address": data['address'],
        "delivery_type": data['delivery_type'],
        "payment_method": data['payment_method'],
        "status": "Pending",
        "date": datetime.datetime.utcnow()
    }
    result = orders.insert_one(order)
    order['_id'] = str(result.inserted_id)
    return jsonify(order), 201

@orders_bp.route('/', methods=['GET'])
@token_required
def get_orders():
    if request.user['role'] == 'buyer':
        result = list(orders.find({'buyer_id': request.user['id']}))
    elif request.user['role'] == 'farmer':
        result = list(orders.find({'products.farmer_id': request.user['id']}))
    else:
        result = list(orders.find())

    for o in result:
        o['_id'] = str(o['_id'])
    return jsonify(result)

@orders_bp.route('/<id>/cancel', methods=['PUT'])
@token_required
def cancel_order(id):
    if request.user['role'] != 'buyer':
        return jsonify({'error': 'Access denied'}), 403

    result = orders.update_one({'_id': ObjectId(id), 'buyer_id': request.user['id']}, {"$set": {"status": "Cancelled"}})
    if result.matched_count == 0:
        return jsonify({'error': 'Not found or not allowed'}), 404
    return jsonify({'message': 'Order cancelled'})

@orders_bp.route('/<id>/deliver', methods=['PUT'])
@token_required
def mark_delivered(id):
    if request.user['role'] != 'farmer':
        return jsonify({'error': 'Access denied'}), 403

    result = orders.update_one({'_id': ObjectId(id), 'products.farmer_id': request.user['id']}, {"$set": {"status": "Delivered"}})
    if result.matched_count == 0:
        return jsonify({'error': 'Not found or not allowed'}), 404
    return jsonify({'message': 'Order marked as delivered'})
