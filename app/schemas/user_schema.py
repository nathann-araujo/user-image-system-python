from pydantic import BaseModel


class UserBase(BaseModel):
    username: str


class UserCreate(UserBase):
    pass


class UserUpdate(UserBase):
    id: int


class UserImage(BaseModel):
    user_id: int
    image_id: int


class UserImageUpdate(UserImage):
    image: str


class User(UserBase):
    id: int
    images: list["Image"] = []

    class Config:
        orm_mode = True
