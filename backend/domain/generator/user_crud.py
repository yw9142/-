from datetime import datetime
from sqlalchemy.orm import Session

from domain.generator.generator_schema import UserCreate

from models import User


def get_user_list(db: Session):
    user_list = db.query(User) \
        .order_by(User.service_number.asc()) \
        .all()
    return user_list


def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    return user


def create_user(db: Session, user_create: UserCreate):
    db_user = User(name=user_create.name,
                   service_number=user_create.service_number,
                   create_date=datetime.now())

    db.add(db_user)
    db.commit()


#   Session.query(db_user).order_by(db_user.service_number.desc())

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()
