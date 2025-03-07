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
    
class devil_fruit(BaseModel):
    id: uuid.UUID
    name: str = Field(max_length=40 )
    fruit_type: Fruit_Type
    effect: str = Field(max_length=100)
    current_user: Optional[str] = Field(max_length=40, default=None)
    photo_url: Optional[str] = None
    comments: Optional[str] = Field(max_length=100, default=None)

devil_fruits:List[devil_fruit] = []

characters = []

@app.get("/")
def root():
    return{"Kaizoku ou ni ore wa naru"}

@app.post("/devil_fruit")
def create_fruit(devil_fruit:devil_fruit):
    for existing_devil_fruit in devil_fruits:
        if existing_devil_fruit.name.lower() == devil_fruit.name.lower():
            raise HTTPException(status_code=409, detail="Devil fruit already ") 
        
    new_fruit = devil_fruit.model_copy(update={"id": uuid.uuid4()})
    
    devil_fruits.append(new_fruit)
    
    return new_fruit

    


if __name__ == "__main__":
    import uvicorn

    uvicorn.run(app, host="0.0.0.0", port=8000)