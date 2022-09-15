from sqlalchemy.exc import NoResultFound

from app.crud.base import CRUDBase
from app.exceptions.invalid_b64_image_exception import InvalidB64ImageException
from app.model.image import Image
from app.schemas import image_schema
from app.utils.utils import generate_thumbnail_100


class CRUDImage(CRUDBase):
    def get_image(self, user_id: int, image_id: int) -> Image:
        return self.db.query(Image).filter(Image.owner_id == user_id, Image.id == image_id).first()

    def get_thumbnails(self, user_id: int):
        thumbnails = self.db.query(Image.thumbnail).filter(Image.owner_id == user_id).all()
        thumbnails_list = [t.thumbnail for t in thumbnails]
        return thumbnails_list

    def create_image(self, image: image_schema.ImageCreate, user_id: int):
        db_image = Image(image_b64=image.image_b64, owner_id=user_id)
        try:
            db_image.generate_thumbnail(generate_thumbnail_100)
        except InvalidB64ImageException:
            raise
        self.db.add(db_image)
        self.db.commit()
        self.db.refresh(db_image)
        return db_image.id

    def update_image(self, user_id: int, image_id: int, image64: str):
        db_image = self.get_image(user_id, image_id)
        db_image.image_b64 = image64
        try:
            db_image.generate_thumbnail(generate_thumbnail_100)
        except InvalidB64ImageException:
            raise
        self.db.commit()
        self.db.refresh(db_image)
        return db_image.id

    def delete_image(self, user_id:int, image_id: int):
        db_image = self.get_image(user_id,image_id)
        if db_image:
            self.db.delete(db_image)
            self.db.commit()
        else:
            raise NoResultFound
