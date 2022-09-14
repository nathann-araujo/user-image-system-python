from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session
from app.model.user import User
from app.model.image import Image
from app.schemas import image_schema, user_schema


def get_user(db: Session, user_id: int) -> user_schema.User:
    return db.query(User).filter(User.id == user_id).first()


def get_user_by_username(db: Session, username: str):
    return db.query(User).filter(User.username == username).first()


def get_user_images(db: Session, user_id: int):
    user = get_user(db, user_id)
    images = user.images
    return images


def get_image(db: Session, user_id: int, image_id: int):
    db_image = db.query(Image).filter(Image.owner_id == user_id, Image.id == image_id).first()
    if db_image:
        return db_image
    else:
        raise NoResultFound


def create_user(db: Session, user: user_schema.UserCreate):
    db_user = User(username=user.username)
    db.add(db_user)
    db.commit()
    db.refresh(db_user)
    return db_user


def update_user_username(db: Session, user: user_schema.User, username: str):
    db_user = user
    db_user.username = username
    db.commit()
    db.refresh(db_user)
    return db_user.id


def update_user_image(db: Session, user: user_schema.User, image_id: int, image: str):
    db_image = get_image(db, user_id= user.id, image_id=image_id)
    db_image.image = image
    db.commit()
    db.refresh(db_image)
    return db_image


def create_user_image(db: Session, image: image_schema.ImageCreate, user_id:int):
    db_image = Image(image=image.image, owner_id=user_id)
    db.add(db_image)
    db.commit()
    db.refresh(db_image)
    return db_image


def delete_user_image(db: Session, user_id: int, image_id: int):
    db_image = get_image(db, user_id=user_id, image_id=image_id)
    if db_image:
        db.delete(db_image)
        db.commit()
    else:
        raise NoResultFound
