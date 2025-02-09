from sqlalchemy import String, Column, Integer
from models.base import Base


class User(Base):
    __tablename__ = "users"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    username = Column(String)
    telegram_id = Column(Integer)