from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

class Fruit_Type(str, Enum):
    ZOAN = "zoan"
    PARAMECIA = "paramecia"
    LOGIA = "logia"
    
class Devil_Fruit(BaseModel):
    name: str = Field(max_length=40 )
    fruit_type: Fruit_Type
    effect: str = Field(max_length=150)
    current_user: Optional[str] = Field(max_length=40, default=None)
    photo_url: Optional[str] = None
    comments: Optional[str] = Field(max_length=100, default=None)

class Devil_Fruit_WithID(Devil_Fruit):
    id:uuid.UUID

devil_fruits:List[Devil_Fruit_WithID] = [
    Devil_Fruit_WithID(
        id = uuid.UUID("5a25062e-341c-4e45-9ccb-442746bb7b36"),
        name = "Gomu Gomu no mi",
        fruit_type = "paramecia",
        effect = "Rubber properties for the user",
        current_user = "Monkey D. Luffy",
        photo_url = None,
        comments = "Original name 'Hito Hito no mi: Nika Model’"
    ),
    Devil_Fruit_WithID(
        id = uuid.UUID("b53c5ee1-b0c6-4d38-ac22-36c77df4a318"),
        name = "Hito Hito no mi",
        fruit_type = "zoan",
        effect = "Humans' habilites for the user",
        current_user = "Tony Tony Chopper",
        photo_url = None,
        comments = None
    ),
    Devil_Fruit_WithID(
        id = uuid.UUID("4024e84d-df58-41f7-940b-c820b612698b"),
        name = "Hana Hana no mi",
        fruit_type = "paramecia",
        effect = "Allow the user to bloom body parts on solid surfaces",
        current_user = "Nico robin",
        photo_url = None,
        comments = None
    )
]