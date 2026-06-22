from pydantic import BaseModel
from typing import Optional

class DefaultResponse(BaseModel):
    id: Optional[int]
    msg: str