from src.akuma_no_mi_api.db.database import Base
from sqlalchemy import Column,Integer,String,Enum
from enum import Enum as PyEnum

"""
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
"""
class FruitType(str, PyEnum):
    ZOAN = "zoan"
    PARAMECIA = "paramecia"
    LOGIA = "logia"

class devil_fruit(Base):
    __tablename__= "devil_fruit"

    id = Column(Integer,primary_key=True, autoincrement=True)
    name = Column(String(40),nullable=False)
    fruit_type =Column(Enum(FruitType),nullable=False) #Fruit_Type
    effect = Column(String(150),nullable=False)
    current_user =Column(String(40),nullable=True)
    photo_url = Column(String,nullable=True)
    comments = Column(String(150),nullable=True)
