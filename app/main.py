from fastapi import FastAPI
from app.routers import units, productions

app = FastAPI(title="Demeter", version="0.1.0")


app.include_router(units.router)
app.include_router(productions.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
