from fastapi import APIRouter, HTTPException, Query, status

from api.models.items.crud import create_item, get_all_items, get_item, update_item, delete_item
from api.models.items.schema import Item, UpdateItem
from api.utils.base_response import PaginatedResponse, PaginationItems, BaseResponse, RESPONSE_422

router = APIRouter(
    prefix="/item",
    tags=["Item"]
)

@router.get("", response_model=PaginatedResponse[Item])
async def read_items(
        page: int = Query(1, ge=1, description="Page number"),
        size: int = Query(10, ge=1, le=100, description="Items per page")
):
    paginated_items = await get_all_items(page=page, size=size)
    return PaginatedResponse[Item](
        status_code=200,
        message="Items retrieved successfully.",
        result=paginated_items
    )

@router.post("", status_code=status.HTTP_201_CREATED, response_model=BaseResponse[Item], responses={422: RESPONSE_422})
async def add_item(item: Item):
    created_item = await create_item(item.dict())
    if created_item is None:
        raise HTTPException(status_code=400, detail="Failed to create item")
    return BaseResponse[Item](
        status_code=status.HTTP_201_CREATED,
        message="Item created successfully",
        result=created_item
    )

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
