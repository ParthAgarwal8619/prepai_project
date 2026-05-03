from pymongo import MongoClient
from pymongo.errors import ConnectionFailure
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = os.getenv("MONGO_URI", "mongodb://localhost:27017")
DB_NAME = os.getenv("DB_NAME", "prepai")

client = None
db = None

def connect_db():
    global client, db
    try:
        client = MongoClient(MONGO_URI, serverSelectionTimeoutMS=5000)
        client.admin.command("ping")
        db = client[DB_NAME]
        print(f"[DB] Connected to MongoDB → {MONGO_URI} / {DB_NAME}")
        return db
    except ConnectionFailure as e:
        print(f"[DB] MongoDB connection failed: {e}")
        print("[DB] Running without database - using in-memory storage")
        return None

def get_db():
    global db
    if db is None:
        connect_db()
    return db
