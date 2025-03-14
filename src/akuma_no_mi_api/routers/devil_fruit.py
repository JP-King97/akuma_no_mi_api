from typing import Any, Dict, List
from fastapi import APIRouter, Depends, File, HTTPException, UploadFile
from akuma_no_mi_api.repository.devil_fruit import create_df, create_dfs_byFILE, delete_df_byID, get_all_df, get_df_byID, update_df_byID
from src.akuma_no_mi_api.schemas import Devil_Fruit
from src.akuma_no_mi_api.db.database import get_db
from sqlalchemy.orm import Session
import pandas as pd

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

@router.post("/upload_devil_fruits")
async def upload_devil_fruits(file: UploadFile = File(...), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    return await create_dfs_byFILE(file,db)