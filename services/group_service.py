from core.db import groups_collection
from bson import ObjectId
from datetime import datetime

def serialize_group(group):
    group["_id"] = str(group["_id"])
    for msg in group.get("messages", []):
        msg["_id"] = str(msg["_id"])
        msg["timestamp"] = msg["timestamp"].isoformat()
    return group

def create_group(uid: str, name: str):
    new_group = {
        "name": name,
        "creator": uid,
        "members": [uid],
        "messages": []
    }
    result = groups_collection.insert_one(new_group)
    new_group["_id"] = result.inserted_id
    return serialize_group(new_group)

def get_all_groups_basic():
    groups = groups_collection.find({}, {"name": 1, "creator": 1, "members": 1})
    result = []
    for group in groups:
        result.append({
            "_id": str(group["_id"]),
            "name": group["name"],
            "creator": group["creator"],
            "members": group["members"]
        })
    return result

def get_group_if_member(group_id, uid):
    group = groups_collection.find_one({"_id": ObjectId(group_id)})
    if not group or uid not in group["members"]:
        return None
    return group

def join_group(group_id, uid):
    groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$addToSet": {"members": uid}}
    )
    return serialize_group(groups_collection.find_one({"_id": ObjectId(group_id)}))

def add_group_message(group_id, uid, content):
    group = get_group_if_member(group_id, uid)
    if not group:
        return None

    new_msg = {
        "_id": ObjectId(),
        "from_user": uid,
        "content": content,
        "timestamp": datetime.utcnow(),
        "edited": False,
        "deleted": False
    }

    groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$push": {"messages": new_msg}}
    )
    return new_msg

def edit_group_message(group_id, msg_id, uid, new_content=None, deleted=None):
    group = get_group_if_member(group_id, uid)
    if not group:
        return None, "not_found"

    for msg in group["messages"]:
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

    groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$set": {"messages": group["messages"]}}
    )
    return msg, None

def delete_group_message(group_id, msg_id, uid):
    group = get_group_if_member(group_id, uid)
    if not group:
        return None, "not_found"

    for msg in group["messages"]:
        if str(msg["_id"]) == msg_id:
            if msg["from_user"] != uid:
                return None, "unauthorized"
            msg["deleted"] = True
            break
    else:
        return None, "not_found"

    groups_collection.update_one(
        {"_id": ObjectId(group_id)},
        {"$set": {"messages": group["messages"]}}
    )
    return msg, None
