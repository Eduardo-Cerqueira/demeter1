from fastapi import FastAPI,Request
from fastapi.responses import JSONResponse

from app.routers import units, productions, plots, spreads

app = FastAPI(title="Demeter", version="0.1.0")


app.include_router(units.router)
app.include_router(productions.router)
app.include_router(plots.router)
app.include_router(spreads.router)

@app.exception_handler(Exception)
async def validation_exception_handler(request: Request, exc: Exception):
    # Change here to Logger
    return JSONResponse(
        status_code=500,
        content={
            "message": (
                f"Failed method {request.method} at URL {request.url}."
                f" Exception message is {exc!r}."
            )
        },
    )
@app.get("/")
def read_root():
    return {"message": "Hello World"}
