from fastapi import FastAPI
from akuma_no_mi_api.db import models
from akuma_no_mi_api.routers import devil_fruit
from akuma_no_mi_api.db.database import engine
import uvicorn

def create_tables():
    print("Creating tables...")  # Debugging log
    try:
        models.Base.metadata.create_all(engine)
        print("Tables successfully created.") 
    except Exception as e:
        print(f"Error creating table: {e}")

create_tables()

app = FastAPI()
app.include_router(devil_fruit.router)

if __name__ == "__main__":
    uvicorn.run(app, host= "0.0.0.0", port=8000, reload=True)