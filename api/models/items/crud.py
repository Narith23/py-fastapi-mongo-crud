from bson import ObjectId

from api.core.database import items_collection


def item_helper(item) -> dict:
    return {
        "id": str(item["_id"]),
        "name": item["name"],
        "email": item["email"] if "email" in item else None,
        "description": item.get("description") if "description" in item else None,
    }

async def create_item(data: dict) -> dict:
    result = await items_collection.insert_one(data)
    item = await items_collection.find_one({"_id": result.inserted_id})
    return item_helper(item)

async def get_all_items():
    items = []
    async for item in items_collection.find():
        items.append(item_helper(item))
    return items

async def get_item(id: str):
    item = await items_collection.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)

async def update_item(id: str, data: dict):
    await items_collection.update_one({"_id": ObjectId(id)}, {"$set": data})
    item = await items_collection.find_one({"_id": ObjectId(id)})
    if item:
        return item_helper(item)

async def delete_item(id: str):
    result = await items_collection.delete_one({"_id": ObjectId(id)})
    return result.deleted_count > 0
