from typing import TypeVar, Generic, Optional, List
from pydantic import BaseModel, Field
from pydantic.generics import GenericModel

T = TypeVar("T")

RESPONSE_404 = {
    "description": "Item not found",
    "content": {
        "application/json": {
            "example": {
                "status_code": 404,
                "message": "Item not found",
                "result": None
            }
        }
    }
}

RESPONSE_422 = {
    "description": "Validation failed",
    "content": {
        "application/json": {
            "example": {
                "status_code": 422,
                "message": "Validation failed",
                "result": [
                    {
                        "field": "string",
                        "message": "string validation failed",
                    }
                ]
            }
        }
    }
}

class BaseResponse(GenericModel, Generic[T]):
    status_code: int = Field(200, description="HTTP status code")
    message: str = Field("OK", description="Description or message")
    result: Optional[T] = Field(None, description="Returned data (if any)")

class PaginationItems(GenericModel, Generic[T]):
    data: List[T] = Field(default_factory=list, description="Paginated list of items")
    page: int = Field(..., ge=1, description="Current page number")
    size: int = Field(..., ge=1, description="Items per page")
    total: int = Field(..., ge=0, description="Total number of items")
    pages: int = Field(..., ge=0, description="Total number of pages")


class PaginatedResponse(GenericModel, Generic[T]):
    status_code: int = Field(200, description="HTTP status code")
    message: str = Field("OK", description="Description or message")
    result: Optional[PaginationItems[T]] = Field(None, description="Paginated result data")
