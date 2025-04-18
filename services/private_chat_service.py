from core.db import private_chats_collection
from bson import ObjectId
from datetime import datetime

def serialize_chat(chat):
    chat["_id"] = str(chat["_id"])
    for msg in chat.get("messages", []):
        msg["_id"] = str(msg["_id"])
        msg["timestamp"] = msg["timestamp"].isoformat()
    return chat

def create_private_chat(uid: str, other_uid: str):
    existing = private_chats_collection.find_one({
        "members": {"$all": [uid, other_uid], "$size": 2}
    })
    if existing:
        return {"message": "Chat already exists", "chat": serialize_chat(existing)}

    new_chat = {
        "members": [uid, other_uid],
        "messages": [],
    }

    result = private_chats_collection.insert_one(new_chat)
    new_chat["_id"] = result.inserted_id
    return {"message": "Private chat created", "chat": serialize_chat(new_chat)}

def get_chat_if_member(chat_id, uid):
    chat = private_chats_collection.find_one({"_id": ObjectId(chat_id)})
    if not chat or uid not in chat["members"]:
        return None
    return chat

def add_message(chat_id, uid, content):
    chat = get_chat_if_member(chat_id, uid)
    if not chat:
        return None

    new_msg = {
        "_id": ObjectId(),
        "from_user": uid,
        "content": content,
        "timestamp": datetime.utcnow(),
        "edited": False,
        "deleted": False
    }

    private_chats_collection.update_one(
        {"_id": ObjectId(chat_id)},
        {"$push": {"messages": new_msg}}
    )
    return new_msg

def edit_message(chat_id, msg_id, uid, new_content=None, deleted=None):
    chat = get_chat_if_member(chat_id, uid)
    if not chat:
        return None, "not_found"

    for msg in chat["messages"]:
        if str(msg["_id"]) == msg_id:
            if msg["from_user"] != uid:
                return None, "unauthorized"
            if new_content is not None:
                msg["content"] = new_content
                msg["edited"] = True
            if deleted is not None:
                msg["deleted"] = deleted
            break
    else:
        return None, "not_found"

    private_chats_collection.update_one(
        {"_id": ObjectId(chat_id)},
        {"$set": {"messages": chat["messages"]}}
    )
    return msg, None

def delete_message(chat_id, msg_id, uid):
    chat = get_chat_if_member(chat_id, uid)
    if not chat:
        return None, "not_found"

    for msg in chat["messages"]:
        if str(msg["_id"]) == msg_id:
            if msg["from_user"] != uid:
                return None, "unauthorized"
            msg["deleted"] = True
            break
    else:
        return None, "not_found"

    private_chats_collection.update_one(
        {"_id": ObjectId(chat_id)},
        {"$set": {"messages": chat["messages"]}}
    )
    return msg, None