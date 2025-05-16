from motor.motor_asyncio import AsyncIOMotorClient
from api.core.config import DATABASE_URI, DATABASE_NAME

# MongoDB connection
client = AsyncIOMotorClient(DATABASE_URI)

# Access the correct database
database = client[DATABASE_NAME]

# Define collections
items_collection = database.get_collection("items")