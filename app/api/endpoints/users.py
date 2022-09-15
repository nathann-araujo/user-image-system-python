from fastapi import APIRouter, HTTPException, Depends

from app.crud.crud_user import CRUDUser
from app.schemas import user_schema


router = APIRouter()


@router.post("/", status_code=201)
def add_user(user: user_schema.UserCreate, crud_user: CRUDUser = Depends(CRUDUser)):
    db_user = crud_user.find_user_by_username(user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already exist")
    user_id = crud_user.create_user(user)

    return {"user_id": user_id}


@router.put("/{user_id}")
def update_user(user_id:int, user: user_schema.UserUpdate, crud_user: CRUDUser = Depends(CRUDUser)):
    db_user = crud_user.find_user_by_id(user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")

    if crud_user.find_user_by_username(user.username):
        raise HTTPException(status_code=400, detail="Username already exist")

    user_updated_id = crud_user.update_user(user_id, user)

    return {"user_id": user_updated_id}


