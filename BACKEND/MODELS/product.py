# server/models/product.py

def format_product(product):
    return {
        "id": str(product["_id"]),
        "name": product["name"],
        "description": product["description"],
        "price": product["price"],
        "category": product["category"],
        "stock": product["stock"],
        "farmer_id": product["farmer_id"]
    }

def validate_product_data(data):
    return all(key in data for key in ("name", "description", "price", "category", "stock"))
