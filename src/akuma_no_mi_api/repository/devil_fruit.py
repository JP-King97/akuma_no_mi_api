
from io import BytesIO
from typing import Any, Dict, List
from fastapi import Depends, File, HTTPException, UploadFile
import pandas as pd
from sqlalchemy import text, update
from sqlalchemy.orm import Session
from akuma_no_mi_api.db import models
from akuma_no_mi_api.db.database import get_db
from akuma_no_mi_api.routers import devil_fruit
from src.akuma_no_mi_api.schemas import Devil_Fruit

def df_query(db:Session):
    return db.query(models.devil_fruits)

def get_all_df(db:Session):
    return  df_query(db).all()

def create_df(devil_fruit:devil_fruit,db:Session):
    df = devil_fruit.model_dump()
    existing_df = df_query(db).filter(
        (models.devil_fruits.id == df["id"]) | (models.devil_fruits.name == df["name"])
    ).first()

    result = db.execute(text("SELECT setval('devil_fruits_id_seq', COALESCE((SELECT MAX(id) FROM devil_fruits), 1), false);"))
    next_id = result.scalar() + 1

    if existing_df:
        if df["id"]:
            if existing_df.id == df["id"]:
                raise HTTPException(status_code=400, detail="A devil fruit with this ID already exists.")
        if existing_df.name == df["name"]:
            raise HTTPException(status_code=400, detail="A devil fruit with this name already exists.")

    new_df = models.devil_fruits(
        id = df["id"] if df["id"] is not None else next_id,
        name = df["name"],
        fruit_type = df["fruit_type"],
        effect = df["effect"],
        current_user = df["current_user"],
        cannon = df["cannon"],
        photo_url = df["photo_url"],
        comments = df["comments"]
    )
    
    db.add(new_df)
    db.commit()
    db.refresh(new_df)
    return Devil_Fruit.model_validate(devil_fruit)

def get_df_byID(devil_fruit_id:int, db:Session):
    data = df_query(db).filter(models.devil_fruits.id == devil_fruit_id).first()
    if data is None:
        raise HTTPException(status_code=404, detail="A devil fruit id not found")
    else:
        return data 

def update_df_byID(devil_fruit_id:int,updated_devil_fruit_info:devil_fruit,db:Session):
    if not df_query(db).filter(models.devil_fruits.id == devil_fruit_id).first():
       raise HTTPException(status_code=404, detail="A devil fruit id not found")
    if df_query(db).filter((models.devil_fruits.id == updated_devil_fruit_info.id) & (updated_devil_fruit_info.id != devil_fruit_id)).first():
       raise HTTPException(status_code=404, detail="A devil fruit with this id already exists. ")  
    if df_query(db).filter((updated_devil_fruit_info.name == models.devil_fruits.name) & (models.devil_fruits.id != devil_fruit_id)).first():
       raise HTTPException(status_code=400, detail="A devil fruit with this name already exists.")
    db.execute(
        update(models.devil_fruits)
        .where(models.devil_fruits.id == devil_fruit_id)
        .values(**updated_devil_fruit_info.model_dump(exclude_unset=True))
    )
    db.commit()
    return updated_devil_fruit_info

def delete_df_byID(devil_fruit_id:int,db:Session):
    df = df_query(db).filter(models.devil_fruits.id == devil_fruit_id).first()
    if df is None:
        raise HTTPException(status_code=404, detail="A devil fruit id not found")
    df_name = df.name
    db.delete(df)
    db.commit()
    return f"A devil fruit {df_name} was deleted."

async def create_dfs_byFILE(file: UploadFile = File(...), db: Session = Depends(get_db)) -> List[Dict[str, Any]]:
    # Verify the fileType (xlsx)
    if not file.filename.endswith(".xlsx"):
        raise HTTPException(status_code=400, detail="Only XLSX files are supported.")

    # Read the XLSX file into a DataFrame
    contents = await file.read()
    df = pd.read_excel(BytesIO(contents))

    # Verify all the properties/columns, are in the file
    required_columns = {"id", "name", "fruit_type", "effect", "current_user","cannon", "photo_url", "comments"}
    if not required_columns.issubset(df.columns):
        raise HTTPException(status_code=400, detail=f"Missing required columns: {required_columns - set(df.columns)}")

    responses = []
    for _,row in df.iterrows():
        devil_fruit_data = row.to_dict()
        # Convert NaN values to NoneSS
        devil_fruit_data = {key: (None if pd.isna(value) else value) for key, value in devil_fruit_data.items()}
        try:
            # Create Devil_Fruit instance
            devil_fruit = Devil_Fruit(**devil_fruit_data)
            # Call create function
            new_df = create_df(devil_fruit, db)
            responses.append({"status": "success", "data": new_df})
        except HTTPException as e:
            responses.append({"status": "error", "error": e.detail})

    return responses