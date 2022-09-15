from fastapi import Depends
from sqlalchemy.orm import Session

from app.crud.dependencies import get_db


class CRUDBase:
    def __init__(self, db: Session = Depends(get_db)):
        self.db = db
