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


@router.delete("/delete", status_code=status.HTTP_204_NO_CONTENT)
def user_delete(_user_delete: generator_schema.UserDelete, db: Session = Depends(get_db)):
    #    current_user: User = Depends(get_current_user)):
    db_user = user_crud.get_user(db, user_id=_user_delete.user_id)
    if not db_user:
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST,
                            detail="데이터를 찾을수 없습니다.")
    user_crud.delete_user(db=db, db_user=db_user)
