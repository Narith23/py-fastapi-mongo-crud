from pydantic import BaseModel, EmailStr
from typing import Optional

class Item(BaseModel):
    id: Optional[str] = None
    name: str
    email: Optional[EmailStr] = None
    description: Optional[str] = None

class CreateItem(Item):
    pass

class UpdateItem(BaseModel):
    name: Optional[str]
    email: Optional[EmailStr] = None
    description: Optional[str] = None
