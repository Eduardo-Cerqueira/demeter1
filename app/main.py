from fastapi import FastAPI, Request

from app.routers import plots

app = FastAPI()


app.include_router(plots.router)


@app.get("/")
def read_root():
    return {"message": "Hello World"}
