from fastapi import APIRouter, HTTPException, Query, status
from bson.errors import InvalidId

from api.models.items.crud import (
    create_item,
    get_all_items,
    get_item,
    update_item,
    delete_item
)
from api.models.items.schema import Item, UpdateItem
from api.utils.base_response import (
    PaginatedResponse,
    PaginationItems,
    BaseResponse,
    RESPONSE_422,
    RESPONSE_400,
    RESPONSE_404
)

router = APIRouter(
    prefix="/item",
    tags=["Item"]
)


@router.get("", response_model=PaginatedResponse[Item], status_code=status.HTTP_200_OK)
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


@router.post(
    "",
    status_code=status.HTTP_201_CREATED,
    response_model=BaseResponse[Item],
    responses={400: RESPONSE_400, 422: RESPONSE_422},
    description="Create an item"
)
async def add_item(item: Item):
    created_item = await create_item(item.dict())
    return BaseResponse[Item](
        status_code=status.HTTP_201_CREATED,
        message="Item created successfully",
        result=created_item
    )


@router.get(
    "/{item_id}",
    response_model=BaseResponse[Item],
    status_code=status.HTTP_200_OK,
    responses={404: RESPONSE_404},
    description="Get item by ID"
)
async def read_item(item_id: str):
    try:
        item = await get_item(item_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid item ID")
    return BaseResponse[Item](
        status_code=status.HTTP_200_OK,
        message="Item retrieved successfully",
        result=item
    )


@router.put(
    "/{item_id}",
    response_model=BaseResponse[Item],
    status_code=status.HTTP_200_OK,
    responses={404: RESPONSE_404, 400: RESPONSE_400, 422: RESPONSE_422},
    description="Update item"
)
async def edit_item(item_id: str, item: UpdateItem):
    try:
        updated_item = await update_item(item_id, item.dict(exclude_unset=True))
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid item ID")
    return BaseResponse[Item](
        status_code=status.HTTP_200_OK,
        message="Item updated successfully",
        result=updated_item
    )


@router.delete("/{item_id}", status_code=status.HTTP_200_OK)
async def remove_item(item_id: str):
    try:
        success = await delete_item(item_id)
    except InvalidId:
        raise HTTPException(status_code=404, detail="Invalid item ID")
    if not success:
        raise HTTPException(status_code=404, detail="Item not found")
    return BaseResponse(
        status_code=status.HTTP_200_OK,
        message="Item deleted successfully",
        result=None
    )
