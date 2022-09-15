from typing import Type

from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.base import CRUDBase
from app.db.database import SessionLocal


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


def get_crud(crud: Type[CRUDBase]):
    def get_crud_rep(db: Session = Depends(get_db)):
        return crud(db)
    return get_crud_rep
