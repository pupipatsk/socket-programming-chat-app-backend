from core.db import users_collection

def serialize_user(user):
    user["_id"] = str(user["_id"])
    return user

def get_user_by_uid(uid: str):
    user = users_collection.find_one({"uid": uid})
    if not user:
        return None
    return serialize_user(user)

def create_user_if_not_exists(uid: str, email: str, name: str):
    existing = users_collection.find_one({"uid": uid})
    if existing:
        return {"message": "User already exists", "user": serialize_user(existing)}

    user = {
        "uid": uid,
        "email": email,
        "name": name,
        "status": "Online",
        "private_chats": [],
        "groups": []
    }

    result = users_collection.insert_one(user)
    user["_id"] = result.inserted_id
    return {"message": "User created", "user": serialize_user(user)}

def get_users_by_status(status: str):
    users = users_collection.find({"status": status})
    return [serialize_user(user) for user in users]

def update_user_fields(uid: str, name: str = None, status: str = None):
    update_data = {}
    if name:
        update_data["name"] = name
    if status:
        update_data["status"] = status

    if not update_data:
        return None

    users_collection.update_one({"uid": uid}, {"$set": update_data})
    user = users_collection.find_one({"uid": uid})
    return serialize_user(user)
