from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

MONGO_URI = ""
client = MongoClient(MONGO_URI)

db = client["wellness_db"]
chat_collection = db["chat_history"]
