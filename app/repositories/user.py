from typing import Optional

from app.repositories.base import BaseRepository
from app.schemas import user_schema
from app.model.user import User


class UserRepository(BaseRepository):
    def create_user(self, new_user: user_schema.UserCreate ) -> Optional[User]:
        db_user = User(username=new_user.username)
        self.db.add(db_user)
        self.db.commit()
        self.db.refresh(db_user)
        return db_user
