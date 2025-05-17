import math
from typing import Optional

from bson import ObjectId

from api.core.database import items_collection
from api.models.items.schema import Item
from api.utils.base_response import PaginationItems


def item_helper(item) -> Item:
    return Item(
        id=str(item["_id"]),
        name=item["name"],
        email=item.get("email"),
        description=item.get("description")
    )

async def get_all_items(page: int = 1, size: int = 100) -> PaginationItems[Item]:
    skip = (page - 1) * size
    total = await items_collection.count_documents({})
    cursor = items_collection.find().skip(skip).limit(size)

    items = [item_helper(doc) async for doc in cursor]
    pages = math.ceil(total / size) if size else 0

    return PaginationItems[Item](
        data=items,
        page=page,
        size=size,
        total=total,
        pages=pages
    )

async def create_item(data: dict) -> Optional[Item]:
    result = await items_collection.insert_one(data)
    if not result.inserted_id:
        return None
    item = await items_collection.find_one({"_id": result.inserted_id})
    if item:
        return item_helper(item)
    return None

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
