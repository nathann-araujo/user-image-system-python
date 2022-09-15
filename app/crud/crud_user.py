from app.crud.base import CRUDBase
from app.model.user import User
from app.schemas.user_schema import UserCreate, UserUpdate


class CRUDUser(CRUDBase):

    def find_user_by_username(self, username:str):
        db_user = self.db.query(User).filter(User.username == username).first()
        return db_user

    def find_user_by_id(self, user_id: str):
        db_user = self.db.query(User).filter(User.id == user_id).first()
        return db_user

    def create_user(self,user: UserCreate):
        db_user = User(username=user.username)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user.id

    def update_user(self, user_id:int, user: UserUpdate):
        user_db = self.db.query(User).filter(User.id == user_id).first()
        user_db.username = user.username
        self.db.commit()
        self.db.refresh(user_db)
        return user_db.id

