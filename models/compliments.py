from sqlalchemy import Column, Integer, String

from models.base import Base


class Compliment(Base):
    __tablename__ = 'compliments'
    id = Column(Integer, primary_key=True)
    text = Column(String, unique=True)
