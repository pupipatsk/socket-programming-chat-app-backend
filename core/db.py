from pymongo import MongoClient
from core.config import MONGODB_URI

client = MongoClient(MONGODB_URI)
db = client["myapp"]
users_collection = db["users"]
private_chats_collection = db["private-chats"]
groups_collection = db["groups"]
