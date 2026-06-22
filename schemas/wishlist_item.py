from typing import Optional
from pydantic import BaseModel
from utils.models import OrmBase, ResponseBase

class WishlistItemCreate(BaseModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    sort_order: Optional[int] = None

class WishlistItemUpdate(BaseModel):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    sort_order: Optional[int] = None
    purchased: Optional[bool] = None

class WishlistItemResponse(OrmBase):
    name: str
    description: Optional[str] = None
    link: Optional[str] = None
    sort_order: Optional[int] = None
    purchased: bool

class WishlistItemList(ResponseBase):
    items: list[WishlistItemResponse]