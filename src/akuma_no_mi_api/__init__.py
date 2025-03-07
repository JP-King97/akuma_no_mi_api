from enum import Enum
from typing import List, Optional
from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import uuid

app = FastAPI()

class Fruit_Type(str, Enum):
    ZOAN = "zoan"
    PARAMECIA = "paramecia"
    LOGIA = "logia"
    
class Devil_Fruit(BaseModel):
    name: str = Field(max_length=40 )
    fruit_type: Fruit_Type
    effect: str = Field(max_length=100)
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

characters = []

@app.get("/")
def root():
    return{"Kaizoku ou ni ore wa naru"}

@app.get("/devil_fruits", response_model=List[Devil_Fruit_WithID])
def get_all_fruits():
    return devil_fruits

@app.post("/devil_fruit", response_model=Devil_Fruit_WithID)
def create_fruit(devil_fruit:Devil_Fruit):
    for existing_devil_fruit in devil_fruits:
        if existing_devil_fruit.name.lower() == devil_fruit.name.lower():
            raise HTTPException(status_code=409, detail="Devil fruit already exists") 
        
    new_fruit = Devil_Fruit_WithID(id=uuid.uuid4(), **devil_fruit.model_dump())
    
    devil_fruits.append(new_fruit)
    
    return new_fruit

@app.get("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit_WithID)
def get_fruit_by_id(devil_fruit_id:uuid.UUID):
    for devil_fruit in devil_fruits:
        if devil_fruit.id == devil_fruit_id:
            return devil_fruit
    raise HTTPException(status_code=404, detail= "Devil fruit id not found")

@app.patch("/devil_fruit/{devil_fruit_id}",response_model=Devil_Fruit_WithID)
def update_devil_fruit_by_id(devil_fruit_id:uuid.UUID,updated_devil_fruit_info:Devil_Fruit):
    for index, devil_fruit in enumerate(devil_fruits):
        if devil_fruit.id == devil_fruit_id:
            updated_devil_fruit = Devil_Fruit_WithID(id=devil_fruit_id,**updated_devil_fruit_info.model_dump())

            devil_fruits[index] = updated_devil_fruit
            return updated_devil_fruit
    raise HTTPException(status_code=404, detail= "Devil fruit id not found")

@app.delete("/devil_fruit/{devil_fruit_id}",response_model=str)
def delete_devil_fruit_by_id(devil_fruit_id:uuid.UUID):
    for index, devil_fruit in enumerate(devil_fruits):
        if devil_fruit.id == devil_fruit_id:
            devil_fruits.pop(index)
            return f"Devil fruit {devil_fruit.name} was deleted."
    raise HTTPException(status_code=404, detail= "Devil fruit id not found.")

if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)