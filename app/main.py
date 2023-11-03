from fastapi import FastAPI
from app.routers import fertilizers

app = FastAPI()

app.include_router(fertilizers.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
