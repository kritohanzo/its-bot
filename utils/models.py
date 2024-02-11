from sqlalchemy.orm import DeclarativeBase, relationship
from sqlalchemy import String, Column, Integer, Boolean, Table, ForeignKey


class Base(DeclarativeBase):
    pass


class User(Base):
    __tablename__ = "user"
    id = Column(Integer, primary_key=True)
    first_name = Column(String)
    last_name = Column(String)
    full_name = Column(String)
    username = Column(String)
    telegram_id = Column(Integer)

class AnonymousMessage(Base):
    __tablename__ = "anonymous_message"
    id = Column(Integer, primary_key=True)
    sender_id = Column(ForeignKey("user.id"))
    recipient_id = Column(ForeignKey("user.id"))
    text = Column(String)

class Compliment(Base):
    __tablename__ = "compliment"
    id = Column(Integer, primary_key=True)
    text = Column(String)