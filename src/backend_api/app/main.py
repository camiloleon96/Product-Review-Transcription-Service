from typing import Union
from fastapi import FastAPI
from .models import models
from .database.database import engine
from app.routers import healthcheck
from app.routers import transcription

#Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI()


app.include_router(transcription.router, prefix="/api")
app.include_router(healthcheck.router, prefix="/api")