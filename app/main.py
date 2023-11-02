from fastapi import FastAPI, Request
from fastapi.responses import JSONResponse
from app.routers import units

app = FastAPI(title="Demeter", version="0.1.0")


app.include_router(units.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
