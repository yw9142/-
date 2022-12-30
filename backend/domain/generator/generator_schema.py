import datetime

from pydantic import BaseModel, validator


class User(BaseModel):
    id: int
    name: str
    service_number: str
    create_date: datetime.datetime

    class Config:
        orm_mode = True


class UserCreate(BaseModel):
    name: str
    service_number: str

    @validator('name', 'service_number')
    def not_empty(cls, v):
        if not v or not v.strip():
            raise ValueError('빈 값은 허용되지 않습니다.')
        return v
