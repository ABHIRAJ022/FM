# server/routes/admin.py
from flask import Blueprint, jsonify
from pymongo import MongoClient
import jwt
import os
from functools import wraps

admin_bp = Blueprint('admin', __name__)
client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()
users = db.users
orders = db.orders

def admin_required(f):
    @wraps(f)
    def wrapper(*args, **kwargs):
        token = request.headers.get('Authorization')
        if not token:
            return jsonify({'error': 'Token missing'}), 403
        try:
            data = jwt.decode(token, os.getenv("JWT_SECRET"), algorithms=["HS256"])
            if data['role'] != 'admin':
                return jsonify({'error': 'Access denied'}), 403
            request.user = data
        except:
            return jsonify({'error': 'Invalid token'}), 403
        return f(*args, **kwargs)
    return wrapper

@admin_bp.route('/users', methods=['GET'])
@admin_required
def list_users():
    all_users = list(users.find())
    for u in all_users:
        u['_id'] = str(u['_id'])
    return jsonify(all_users)

@admin_bp.route('/orders', methods=['GET'])
@admin_required
def list_all_orders():
    all_orders = list(orders.find())
    for o in all_orders:
        o['_id'] = str(o['_id'])
    return jsonify(all_orders)

@admin_bp.route('/report', methods=['GET'])
@admin_required
def sales_report():
    total_orders = orders.count_documents({})
    total_sales = sum(order.get('total', 0) for order in orders.find())
    return jsonify({
        "total_orders": total_orders,
        "total_sales": total_sales
    })
