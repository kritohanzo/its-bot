from database.models import Base
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import Session
from contextlib import contextmanager


engine = create_engine("sqlite:///db.sqlite3")


class Database:

    @classmethod
    @contextmanager
    def session(cls):
        session = Session(engine)
        yield session
        session.close()

    @classmethod
    def check_exists_db(cls):
        if not os.path.exists('db.sqlite3'):
            Base.metadata.create_all(bind=engine)