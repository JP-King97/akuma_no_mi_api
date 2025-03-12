
from fastapi import HTTPException
from sqlalchemy import text, update
from sqlalchemy.orm import Session
from akuma_no_mi_api.db import models
from akuma_no_mi_api.routers import devil_fruit

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
        photo_url = df["photo_url"],
        comments = df["comments"]
    )
    
    db.add(new_df)
    db.commit()
    db.refresh(new_df)
    return new_df

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