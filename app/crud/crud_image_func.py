from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from app.model.image import Image
from app.schemas import image_schema, user_schema


def get_image(db: Session, user_id: int, image_id: int):
    db_image = db.query(Image).filter(Image.owner_id == user_id, Image.id == image_id).first()
    if db_image:
        return db_image
    else:
        raise NoResultFound


def update_image(db: Session, user: user_schema.User, image_id: int, image: str):
    db_image = get_image(db, user_id=user.id, image_id=image_id)
    db_image.image = image
    db.commit()
    db.refresh(db_image)
    return db_image


def create_image(db: Session, image: image_schema.ImageCreate, user_id:int):
    db_image = Image(image=image.image, owner_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_image(db: Session, user_id: int, image_id: int):
    db_image = get_image(db, user_id=user_id, image_id=image_id)
    if db_image:
        db.delete(db_image)
        db.commit()
    else:
        raise NoResultFound
