from sqlalchemy.exc import NoResultFound

from app.crud.base import CRUDBase
from app.model.image import Image
from app.schemas import image_schema


class CRUDImage(CRUDBase):
    def get_image(self, user_id: int, image_id: int) -> Image:
        return self.db.query(Image).filter(Image.owner_id == user_id, Image.id == image_id).first()

    def create_image(self, image: image_schema.ImageCreate, user_id: int):
        db_image = Image(image=image.image, owner_id=user_id)
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)
        return db_image

    def update_image(self, user_id: int, image_id: int, image64: str):
        db_image = self.get_image(user_id, image_id)
        db_image.image = image64
        self.db.commit()
        self.db.refresh(db_image)
        return db_image

    def delete_image(self, user_id:int, image_id: int):
        db_image = self.get_image(user_id,image_id)
        if db_image:
            self.db.delete(db_image)
            self.db.commit()
        else:
            raise NoResultFound
