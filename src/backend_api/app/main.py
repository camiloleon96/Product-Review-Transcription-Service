from typing import Union
from fastapi import FastAPI
from . import models
from .database import engine
from app.routers import healthcheck

#Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()

@app.get("/")
def read_root():
    return {"Hello There": "General Kenobi"}

app.include_router(healthcheck.router, prefix="/api")