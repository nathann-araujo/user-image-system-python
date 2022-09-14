from typing import Type

from fastapi import Depends
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker, Session
from app.crud.base import CRUDBase
# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"


SQLALCHEMY_DATABASE_URL = "postgresql://admin:admpass@localhost:5432/image_system"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


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
