from sqlalchemy.orm import Session


class BaseRepository:
    def __int__(self, db: Session):
        self.db = db
