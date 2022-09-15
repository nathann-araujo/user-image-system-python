from pydantic import BaseModel, constr, Field


class UserBase(BaseModel):
    username: str = Field(max_length=75)


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    pass


class User(UserBase):
    id: int
    images: list["Image"] = []

    class Config:
        orm_mode = True
