from fastapi import HTTPException, Depends, APIRouter
from sqlalchemy.exc import NoResultFound
from app.crud.crud_image import CRUDImage
from app.crud.crud_user import CRUDUser
from app.exceptions.invalid_b64_image_exception import InvalidB64ImageException
from app.schemas import image_schema


router = APIRouter()


@router.post("/{user_id}/image", status_code=201)
def add_user_image(user_id: int, image: image_schema.ImageCreate, crud_image: CRUDImage = Depends(CRUDImage),
                   crud_user: CRUDUser = Depends(CRUDUser)):
    db_user = crud_user.find_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    try:
        image_id = crud_image.create_image(image, user_id)
    except InvalidB64ImageException:
        raise HTTPException(status_code=400, detail="Invalid base 64 encoded image")
    return {"image_id": image_id}


@router.get("/{user_id}/image/{image_id}")
def get_user_image(user_id: int, image_id: int, crud_image: CRUDImage = Depends(CRUDImage)):
    db_image = crud_image.get_image(user_id, image_id)

    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")

    return {"image": db_image.image_b64}


@router.get("/{user_id}/images-thumbnails")
def list_user_image_thumbnails(user_id: int, crud_image: CRUDImage = Depends(CRUDImage),
                               crud_user: CRUDUser = Depends(CRUDUser)):
    db_user = crud_user.find_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    thumbnails = crud_image.get_thumbnails(user_id)
    return {"thumbnail_list": thumbnails}


@router.put("/{user_id}/image/{image_id}")
def update_user_image(user_id: int, image_id: int, image: image_schema.ImageCreate,
                      crud_image: CRUDImage = Depends(CRUDImage)):
    db_image = crud_image.get_image(user_id, image_id)
    if db_image is None:
        raise HTTPException(status_code=404, detail="Image not found")
    try:
        updated_image_id = crud_image.update_image(user_id,image_id, image.image_b64)
    except InvalidB64ImageException:
         raise HTTPException(status_code=400, detail="Invalid base 64 encoded image")
    return {"image_id": updated_image_id}


@router.delete("/{user_id}/image/{image_id}", status_code=204)
def delete_user_image(user_id: int, image_id: int, crud_image: CRUDImage = Depends(CRUDImage)):
    try:
        crud_image.delete_image(user_id, image_id)
    except NoResultFound:
        raise HTTPException(status_code=404, detail="Image not found")
    return
