import math
from typing import Optional

from bson import ObjectId
from bson.errors import InvalidId
from fastapi import HTTPException

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


async def create_item(data: dict) -> Item:
    email = data["email"]
    if await items_collection.find_one({"email": email}):
        raise HTTPException(status_code=400, detail="Email already exists")

    result = await items_collection.insert_one(data)
    inserted = await items_collection.find_one({"_id": result.inserted_id})
    return item_helper(inserted)


async def get_item(id: str) -> Item:
    try:
        oid = ObjectId(id)
    except InvalidId:
        raise
    item = await items_collection.find_one({"_id": oid})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_helper(item)


async def update_item(id: str, data: dict) -> Item:
    try:
        oid = ObjectId(id)
    except InvalidId:
        raise

    if "email" in data:
        existing = await items_collection.find_one({"email": data["email"], "_id": {"$ne": oid}})
        if existing:
            raise HTTPException(status_code=400, detail="Email already exists")

    await items_collection.update_one({"_id": oid}, {"$set": data})
    item = await items_collection.find_one({"_id": oid})
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item_helper(item)


async def delete_item(id: str) -> bool:
    try:
        oid = ObjectId(id)
    except InvalidId:
        raise
    result = await items_collection.delete_one({"_id": oid})
    return result.deleted_count > 0
