# server/models/user.py

def format_user(user):
    return {
        "id": str(user["_id"]),
        "name": user["name"],
        "email": user["email"],
        "role": user["role"]
    }

def validate_user_data(data):
    return "name" in data and "email" in data and "password" in data and "role" in data
