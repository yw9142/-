from datetime import datetime
from sqlalchemy.orm import Session

from domain.generator.generator_schema import UserCreate, UserUpdate

from models import User


def get_user_list(db: Session):
    user_list = db.query(User) \
        .order_by(User.service_number.asc()) \
        .all()
    return user_list


def get_user_name_list(db: Session):
    user_list = db.query(User.name, User.is_there) \
        .order_by(User.service_number.asc()) \
        .all()
    return user_list


def get_user(db: Session, user_id: int):
    user = db.query(User).get(user_id)
    return user


def create_user(db: Session, user_create: UserCreate):
    db_user = User(name=user_create.name,
                   service_number=user_create.service_number,
                   create_date=datetime.now(),
                   is_there=True)

    db.add(db_user)
    db.commit()


def update_user(db: Session, db_user: User,
                user_update: UserUpdate):
    db_user.id = user_update.user_id
    db_user.is_there = user_update.is_there
    db.add(db_user)
    db.commit()


#   Session.query(db_user).order_by(db_user.service_number.desc())

def delete_user(db: Session, db_user: User):
    db.delete(db_user)
    db.commit()

# 1. update (is_there)
# 2. get(clean_up_chart)
