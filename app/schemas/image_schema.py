from pydantic import BaseModel
from app.schemas import user_schema


class ImageBase(BaseModel):
    image: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    owner_id: int
    owner: "User"

    class Config:
        orm_mode = True