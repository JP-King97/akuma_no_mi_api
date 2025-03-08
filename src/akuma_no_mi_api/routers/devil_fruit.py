from typing import List
from fastapi import APIRouter, HTTPException
from src.akuma_no_mi_api.schemas import devil_fruits, Devil_Fruit, Devil_Fruit_WithID
import uuid

router = APIRouter(
    prefix="/devil_fruit",
    tags=["devil_fruits"]
)


@router.get("/devil_fruits", response_model=List[Devil_Fruit_WithID])
def get_all_fruits():
    return devil_fruits

@router.post("/devil_fruit", response_model=Devil_Fruit_WithID)
def create_fruit(devil_fruit:Devil_Fruit):
    for existing_devil_fruit in devil_fruits:
        if existing_devil_fruit.name.lower() == devil_fruit.name.lower():
           raise HTTPException(status_code=409, detail="Devil fruit already exists") 
        
    new_fruit = Devil_Fruit_WithID(id=uuid.uuid4(), **devil_fruit.model_dump())
    
    devil_fruits.append(new_fruit)
    
    return new_fruit

@router.get("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit_WithID)
def get_fruit_by_id(devil_fruit_id:uuid.UUID):
    for devil_fruit in devil_fruits:
        if devil_fruit.id == devil_fruit_id:
            return devil_fruit
    raise HTTPException(status_code=404, detail= "Devil fruit id not found")

@router.patch("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit_WithID)
def update_devil_fruit_by_id(devil_fruit_id:uuid.UUID,updated_devil_fruit_info:Devil_Fruit):
    for index, devil_fruit in enumerate(devil_fruits):
        if devil_fruit.id == devil_fruit_id:
            updated_devil_fruit = Devil_Fruit_WithID(id=devil_fruit_id,**updated_devil_fruit_info.model_dump())

            devil_fruits[index] = updated_devil_fruit
            return updated_devil_fruit
    raise HTTPException(status_code=404, detail= "Devil fruit id not found")

@router.delete("/devil_fruit/{devil_fruit_id}",response_model=str)
def delete_devil_fruit_by_id(devil_fruit_id:uuid.UUID):
    for index, devil_fruit in enumerate(devil_fruits):
        if devil_fruit.id == devil_fruit_id:
            devil_fruits.pop(index)
            return f"Devil fruit {devil_fruit.name} was deleted."
    raise HTTPException(status_code=404, detail= "Devil fruit id not found.")