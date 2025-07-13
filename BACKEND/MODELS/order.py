# server/models/order.py

def format_order(order):
    return {
        "id": str(order["_id"]),
        "buyer_id": order["buyer_id"],
        "products": order["products"],  # list of {product_id, qty}
        "address": order["address"],
        "delivery_type": order["delivery_type"],
        "payment_method": order["payment_method"],
        "status": order["status"],
        "date": order["date"].isoformat() if "date" in order else None
    }

def validate_order_data(data):
    return all(k in data for k in ("products", "address", "delivery_type", "payment_method"))
