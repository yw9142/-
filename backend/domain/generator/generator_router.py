from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session

from database import get_db
from domain.generator import generator_schema, user_crud

router = APIRouter(
    prefix="/api/user",
)


@router.get("/list", response_model=list[generator_schema.User])
def user_list(db: Session = Depends(get_db)):
    _user_list = user_crud.get_user_list(db)
    return _user_list
