from fastapi import APIRouter, HTTPException, Depends

from sqlalchemy.exc import NoResultFound
from sqlalchemy.orm import Session

from app.crud import crud_user
from app.crud.crud_image import CRUDImage
from app.schemas import user_schema, image_schema
from app.db.database import get_db, get_crud
from app.utils.utils import generate_thumbnail_100

router = APIRouter()


@router.post("/add-user", status_code=201)
def add_user(user: user_schema.UserCreate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user_by_username(db, username=user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exist")
    db_user = crud_user.create_user(db, user=user)
    return {"user_id": db_user.id}


@router.put("/update-user")
def update_user(user: user_schema.UserUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user.id)
    if crud_user.get_user_by_username(db, user.username):
        raise HTTPException(status_code=400, detail="Username already exist")
    if db_user:
        user_id = crud_user.update_user_username(db, db_user, username=user.username)
        return {"user_id": user_id}
    raise HTTPException(status_code=404, detail="User not found")


@router.post("/add-user-image/{user_id}")
def add_user_image(image: image_schema.ImageCreate, user_id:int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id)
    if db_user:
        db_image = crud_user.create_user_image(db, image, user_id)
        return {"image_id": db_image.id}
    raise HTTPException(status_code=404, detail="User not found")


@router.get("/get-user/{user_id}/image/{image_id}")
def get_user_image(user_id: int, image_id: int, crud: CRUDImage = Depends(get_crud(CRUDImage))):
    db_image = crud.get_image(user_id, image_id)
    if db_image:
        return {"image": db_image.image}
    raise HTTPException(status_code=404, detail="Image not found")


@router.get("/list-user-images-thumbnails/{user_id}")
def list_user_image_thumbnails(user_id: int, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_id)
    if db_user:
        db_image = crud_user.get_user_images(db, user_id)
        image_list = []
        for image in db_image:
            _image = generate_thumbnail_100(image.image)
            image_list.append(_image)
        return {"image_list": image_list}
    raise HTTPException(status_code=404, detail="User not found")


@router.put("/update-user-image")
def update_user_image(user_image: user_schema.UserImageUpdate, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_image.user_id)
    if db_user:
        try:
            db_image = crud_user.update_user_image(db, db_user, user_image.image_id, user_image.image)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Image not found")

        return db_image.image
    raise HTTPException(status_code=404, detail="User not found")


@router.delete("/delete-user-image", status_code=204)
def delete_user_image(user_image: user_schema.UserImage, db: Session = Depends(get_db)):
    db_user = crud_user.get_user(db, user_image.user_id)
    if db_user:
        try:
            crud_user.delete_user_image(db, db_user.id, user_image.image_id)
        except NoResultFound:
            raise HTTPException(status_code=404, detail="Image not found")
        return
    raise HTTPException(status_code=404, detail="User not found")