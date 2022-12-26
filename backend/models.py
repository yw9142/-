from sqlalchemy import Column, Integer, String, Text, DateTime

from database import Base


class User(Base):
    __tablename__ = "user"

    id = Column(Integer, primary_key=True)
    name = Column(String, nullable=False)
    service_number = Column(String, nullable=False)
    create_date = Column(DateTime, nullable=False)
