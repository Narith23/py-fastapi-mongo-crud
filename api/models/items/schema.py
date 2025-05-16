from pydantic import BaseModel
from typing import Optional

class Item(BaseModel):
    name: str
    description: Optional[str] = None

class UpdateItem(BaseModel):
    name: Optional[str]
    description: Optional[str]
