from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from starlette import status

from database import get_db
from domain.generator import generator_schema, user_crud

router = APIRouter(
    prefix="/api/user",
)


@router.get("/list", response_model=list[generator_schema.User])
def user_list(db: Session = Depends(get_db)):
    _user_list = user_crud.get_user_list(db)
    return _user_list


@router.post("/create/{user_id}", status_code=status.HTTP_204_NO_CONTENT)
def user_create(user_id: int,
                _user_create: generator_schema.UserCreate,
                db: Session = Depends(get_db)):

    # create User
    user = user_crud.get_user_list(db, id=user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    user_crud.create_user(db, user=user, user_create=_user_create)
