from sqlalchemy.orm import sessionmaker
from database.models import Base, User
from sqlalchemy import create_engine
import os


engine = create_engine("sqlite:///db.sqlite3")


class Database:
    session = sessionmaker(autoflush=False, bind=engine)

    @classmethod
    def check_exists_db(cls):
        if not os.path.exists('db.sqlite3'):
            Base.metadata.create_all(bind=engine)

    @classmethod
    def create(cls, object: Base):
        with cls.session(autoflush=False, bind=engine) as db:
            db.add(object)
            db.commit()

    @classmethod
    def get(cls, model, first=False, **kwargs):
        with cls.session(autoflush=False, bind=engine) as db:
            queryset = db.query(model)
            for key, value in kwargs.items():
                queryset = queryset.filter(getattr(model, key) == value)
            if first:
                return queryset.first()
            return queryset.all()

    @classmethod
    def delete(cls, object):
        with cls.session(autoflush=False, bind=engine) as db:
            db.delete(object)
            db.commit()

    @classmethod
    def edit(cls, object, **kwargs):
        with cls.session(autoflush=False, bind=engine) as db:
            object = db.query(object.__class__).get(object.id)
            for key, value in kwargs.items():
                setattr(object, key, value)
            db.commit()