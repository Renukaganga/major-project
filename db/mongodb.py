# db/mongodb.py

from pymongo import MongoClient

# Change this if using MongoDB Atlas
MONGO_URI = "mongodb://localhost:27017/"
DB_NAME = "missing_child_finder"

client = MongoClient(MONGO_URI)
db = client[DB_NAME]

# Collections
users_col = db["users"]
missing_col = db["missing_children"]
found_col = db["found_children"]

# ---------- USER ----------
def get_user(email):
    return users_col.find_one({"email": email})

# ---------- MISSING CHILD ----------
def insert_missing_child(data):
    missing_col.insert_one(data)

def get_all_missing():
    return list(missing_col.find())

# ---------- FOUND CHILD ----------
def insert_found_child(data):
    found_col.insert_one(data)

def get_all_found():
    return list(found_col.find())
