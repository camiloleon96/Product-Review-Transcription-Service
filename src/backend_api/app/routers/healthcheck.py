from fastapi import APIRouter
from typing import Annotated
from sqlalchemy.orm import Session
from sqlalchemy import text
from fastapi import Depends
from ..database.database import get_db

router = APIRouter(
    prefix='/healthcheck',
    tags=['healthcheck']
)

db_dependency = Annotated[Session, Depends(get_db)]

@router.get("/db")
def check_db_connection(db: db_dependency):
    db.execute(text("SELECT 1"))
    return {"db": "connected"}