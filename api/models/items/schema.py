from pydantic import BaseModel, EmailStr
from typing import Optional

class Item(BaseModel):
    id: Optional[str]
    name: str
    email: Optional[EmailStr] = None
    description: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr] = None
    description: Optional[str] = None
