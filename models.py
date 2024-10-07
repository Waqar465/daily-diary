from flask_pymongo import ObjectId      
from pymongo import MongoClient

# MongoDB connection setup (replace with your MongoDB URI)
client = MongoClient("mongodb://localhost:27017/")  # For local MongoDB
db = client["daily-diary"]  # Database name
users_collection = db["users"]  # Collection for users
diary_collection = db["diary"]  # Collection for users



class User:
    @staticmethod
    def find_by_username(username):
        return users_collection.find_one({"username": username})
    @staticmethod
    def find_by_id(user_id):
        return users_collection.find_one({"_id": ObjectId(str(user_id))})

    @staticmethod
    def insert_user(username, password):
        return users_collection.insert_one({"username": username, "password": password})

class DiaryEntry:
    @staticmethod
    def insert_entry(user_id, title, content, date):
        return diary_collection.insert_one({
            "user_id": ObjectId(user_id),
            "title": title,
            "content": content,
            "date": date
        })

    @staticmethod
    def get_user_entries(user_id):
        return diary_collection.find({"user_id": ObjectId(user_id)})
