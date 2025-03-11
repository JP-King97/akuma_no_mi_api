from typing import List
from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy import text
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
    data = db.query(models.devil_fruits).all()
    return data

@router.post("/devil_fruit", response_model=Devil_Fruit)
def create_fruit(devil_fruit:Devil_Fruit,db:Session = Depends(get_db)):
    df = devil_fruit.model_dump()
    existing_df = db.query(models.devil_fruits).filter(
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

@router.get("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit)
def get_fruit_by_id(devil_fruit_id:int,db:Session = Depends(get_db)):
    data = db.query(models.devil_fruits).filter(models.devil_fruits.id == devil_fruit_id).first()
    print("query response:",data)
    if data is None:
        raise HTTPException(status_code=404, detail="A devil fruit id not found")
    else:
        return data 

@router.patch("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit)
def update_devil_fruit_by_id(devil_fruit_id:int,updated_devil_fruit_info:Devil_Fruit, db:Session = Depends(get_db)):
   
   df = db.query(models.devil_fruits).filter(models.devil_fruits.id == devil_fruit_id)
   name_check = db.query(models.devil_fruits).filter(updated_devil_fruit_info.name == models.devil_fruits.name)
   print( "name_check = ",name_check)
   if not df.first():
       raise HTTPException(status_code=404, detail="A devil fruit id not found")
   if db.query(models.devil_fruits).filter((models.devil_fruits.id == updated_devil_fruit_info.id) & (updated_devil_fruit_info.id != devil_fruit_id)).first():
       raise HTTPException(status_code=404, detail="A devil fruit with this id already exists. ")  
   if name_check.first():
       raise HTTPException(status_code=400, detail="A devil fruit with this name already exists.")
   df.update(updated_devil_fruit_info.model_dump(exclude_unset=True))
   db.commit()
   return db.query(models.devil_fruits).filter(models.devil_fruits.id == devil_fruit_id).first()

   
    # for index, devil_fruit in enumerate(devil_fruits):
    #     if devil_fruit.id == devil_fruit_id:
    #         updated_devil_fruit = Devil_Fruit(**updated_devil_fruit_info.model_dump())

    #         devil_fruits[index] = updated_devil_fruit
    #         return updated_devil_fruit
    # raise HTTPException(status_code=404, detail= "Devil fruit id not found")

@router.delete("/devil_fruit/{devil_fruit_id}",response_model=str)
def delete_devil_fruit_by_id(devil_fruit_id:int):
    for index, devil_fruit in enumerate(devil_fruits):
        if devil_fruit.id == devil_fruit_id:
            devil_fruits.pop(index)
            return f"A devil fruit {devil_fruit.name} was deleted."
    raise HTTPException(status_code=404, detail= "A devil fruit id not found.")