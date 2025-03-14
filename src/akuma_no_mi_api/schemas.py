from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

class Fruit_Type(str, Enum):
    ZOAN = "Zoan"
    PARAMECIA = "Paramecia"
    LOGIA = "Logia"
    ZOAN_MYTH = "Zoan: Mythical"
    ZOAN_ANCIENT = "Zoan: Ancient"
    ZOAN_ARTIFICIAL = "Zoan: Artificial"
    ZOAN_MYTH_ARTIFICIAL = "Zoan: Artificial Mythical"
    ZOAN_SMILE = "Zoan: Artificial SMILE"
    PARAMECIA_ARTIFICIAL = "Paramecia: Artificial"
    
class Devil_Fruit(BaseModel):
    id:Optional [int] = None
    name: str = Field(max_length=70 )
    fruit_type: Fruit_Type
    effect: str = Field(max_length=150)
    current_user: Optional[str] = Field(max_length=40, default=None)
    cannon:bool
    photo_url: Optional[str] = None
    comments: Optional[str] = Field(max_length=150, default=None)

    class Config:
        from_attributes = True  # Ensures compatibility with SQLAlchemy models
