import datetime

from pydantic import BaseModel


class User(BaseModel):
    id: int
    name: str
    service_number: int
    create_date: datetime.datetime

    class Config:
        orm_mode = True
