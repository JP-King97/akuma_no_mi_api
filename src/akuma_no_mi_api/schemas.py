from enum import Enum
from typing import List, Optional
from pydantic import BaseModel, Field
import uuid

class Fruit_Type(str, Enum):
    ZOAN = "zoan"
    PARAMECIA = "paramecia"
    LOGIA = "logia"
    
class Devil_Fruit(BaseModel):
    id:Optional [int] = None
    name: str = Field(max_length=40 )
    fruit_type: Fruit_Type
    effect: str = Field(max_length=150)
    current_user: Optional[str] = Field(max_length=40, default=None)
    photo_url: Optional[str] = None
    comments: Optional[str] = Field(max_length=150, default=None)

    class Config:
        from_attributes = True  # Ensures compatibility with SQLAlchemy models

devil_fruits:List[Devil_Fruit] = [
    Devil_Fruit(
        id = 1,
        name = "Gomu Gomu no mi",
        fruit_type = "paramecia",
        effect = "Rubber properties for the user",
        current_user = "Monkey D. Luffy",
        photo_url = None,
        comments = "Original name 'Hito Hito no mi: Nika Model’"
    ),
    Devil_Fruit(
        id = 2,
        name = "Hito Hito no mi",
        fruit_type = "zoan",
        effect = "Humans' habilites for the user",
        current_user = "Tony Tony Chopper",
        photo_url = None,
        comments = None
    ),
    Devil_Fruit(
        id = 3,
        name = "Hana Hana no mi",
        fruit_type = "paramecia",
        effect = "blossomed user, Allow the user to bloom body parts on solid surfaces",
        current_user = "Nico robin",
        photo_url = None,
        comments = None
    ),
    Devil_Fruit(
        id = 4,
        name = "Yomi Yomi no mi",
        fruit_type = "paramecia",
        effect = "Resurrected human, enhances the soul of the user granting soul's habilites including getting back from dead",
        current_user = "Brook (Soul King)",
        photo_url = None,
        comments = "Natural enemy of the fruit Soru Soru no mi"
    )

]