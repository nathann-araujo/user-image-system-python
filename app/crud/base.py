from sqlalchemy.orm import Session


class CRUDBase:
    def __init__(self, db: Session):
        self.db = db
