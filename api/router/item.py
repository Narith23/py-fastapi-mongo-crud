from fastapi import APIRouter, HTTPException

from api.models.items.crud import create_item, get_all_items, get_item, update_item, delete_item
from api.models.items.schema import Item, UpdateItem

router = APIRouter(
    prefix="/item",
    tags=["Item"]
)

@router.post("")
async def add_item(item: Item):
    return await create_item(item.dict())

@router.get("")
async def read_items():
    return await get_all_items()

@router.get("/{item_id}")
async def read_item(item_id: str):
    item = await get_item(item_id)
    if not item:
        raise HTTPException(status_code=404, detail="Item not found")
    return item

@router.put("/{item_id}")
async def edit_item(item_id: str, item: UpdateItem):
    updated = await update_item(item_id, item.dict(exclude_unset=True))
    if not updated:
        raise HTTPException(status_code=404, detail="Item not found or not updated")
    return updated

@router.delete("/{item_id}")
async def remove_item(item_id: str):
    success = await delete_item(item_id)
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return {"message": "Item deleted"}
