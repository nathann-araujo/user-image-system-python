from pydantic import BaseModel


class ImageBase(BaseModel):
    image_b64: str


class ImageCreate(ImageBase):
    pass


class Image(ImageBase):
    id: int
    thumbnail: str
    owner_id: int
    owner: "User"

    class Config:
        orm_mode = True