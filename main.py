from fastapi import FastAPI
import uvicorn
from akuma_no_mi_api.routers import devil_fruit

app = FastAPI()
app.include_router(devil_fruit.router)

if __name__ == "__main__":
    uvicorn.run(app, host= "0.0.0.0", port=8000, reload=True)