from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
from akuma_no_mi_api.repository.devil_fruit import create_df, delete_df_byID, get_all_df, get_df_byID, update_df_byID
from src.akuma_no_mi_api.schemas import devil_fruits, Devil_Fruit
from src.akuma_no_mi_api.db.database import get_db
from sqlalchemy.orm import Session
from akuma_no_mi_api.db import models

router = APIRouter(
    prefix="/devil_fruit",
    tags=["devil_fruits"]
)


@router.get("/devil_fruits", response_model=List[Devil_Fruit])
def get_all_fruits(db:Session = Depends(get_db)):
    return get_all_df(db)

@router.post("/devil_fruit", response_model=Devil_Fruit)
def create_devil_fruit(devil_fruit:Devil_Fruit,db:Session = Depends(get_db)):
    return create_df(devil_fruit,db)

@router.get("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit)
def get_fruit_by_id(devil_fruit_id:int,db:Session = Depends(get_db)):
    return get_df_byID(devil_fruit_id,db)

@router.patch("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit)
def update_devil_fruit_by_id(devil_fruit_id:int,updated_devil_fruit_info:Devil_Fruit, db:Session = Depends(get_db)):
   return update_df_byID(devil_fruit_id,updated_devil_fruit_info,db)

@router.delete("/devil_fruit/{devil_fruit_id}",response_model=str)
def delete_devil_fruit_by_id(devil_fruit_id:int, db:Session = Depends(get_db)):
    return delete_df_byID(devil_fruit_id,db)