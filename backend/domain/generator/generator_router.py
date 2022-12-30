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


@router.get("/detail/{user_id}", response_model=generator_schema.User)
def user_detail(user_id: int, db: Session = Depends(get_db)):
    user = user_crud.get_user(db, user_id=user_id)
    return user


@router.post("/create", status_code=status.HTTP_204_NO_CONTENT)
def user_create(_user_create: generator_schema.UserCreate,
                db: Session = Depends(get_db)):
    user_crud.create_user(db=db, user_create=_user_create)
