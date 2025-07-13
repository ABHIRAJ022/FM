from flask import Flask
from flask_cors import CORS
from dotenv import load_dotenv
from pymongo import MongoClient
import os

load_dotenv()

app = Flask(__name__)
CORS(app)

client = MongoClient(os.getenv("MONGO_URI"))
db = client.get_database()

# Blueprints
from ROUTES.auth import auth_bp
from ROUTES.products import products_bp
from ROUTES.orders import orders_bp
from ROUTES.admin import admin_bp

app.register_blueprint(auth_bp, url_prefix='/api/auth')
app.register_blueprint(products_bp, url_prefix='/api/products')
app.register_blueprint(orders_bp, url_prefix='/api/orders')
app.register_blueprint(admin_bp, url_prefix='/api/admin')

if __name__ == "__main__":
    app.run(debug=True)
