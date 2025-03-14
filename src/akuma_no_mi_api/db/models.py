from src.akuma_no_mi_api.db.database import Base
from sqlalchemy import Boolean, Column,Integer,String,Enum
from enum import Enum as PyEnum

class FruitType(str, PyEnum):
    ZOAN = "Zoan"
    PARAMECIA = "Paramecia"
    LOGIA = "Logia"
    ZOAN_MYTH = "Zoan: Mythical"
    ZOAN_ANCIENT = "Zoan: Ancient"
    ZOAN_ARTIFICIAL = "Zoan: Artificial"
    ZOAN_MYTH_ARTIFICIAL = "Zoan: Artificial Mythical"
    ZOAN_SMILE = "Zoan: Artificial SMILE"
    PARAMECIA_ARTIFICIAL = "Paramecia: Artificial"

class devil_fruits(Base):
    __tablename__= "devil_fruits"

    id = Column(Integer,primary_key=True, index=True, autoincrement=True)
    name = Column(String(70),nullable=False)
    fruit_type =Column(Enum(FruitType),nullable=False) #Fruit_Type
    effect = Column(String(150),nullable=False)
    current_user =Column(String(60),nullable=True)
    cannon = Column(Boolean(),nullable=False)
    photo_url = Column(String,nullable=True)
    comments = Column(String(150),nullable=True)
