from utils.models import Base
from sqlalchemy import create_engine
import os
from sqlalchemy.orm import Session
from contextlib import contextmanager
from alembic.config import Config
from alembic import command
from utils.insert_compliments import insert_compliments


engine = create_engine("postgresql+psycopg2://valentine_user:valentine_password@db/valentine_db")


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
            # Base.metadata.create_all(bind=engine)
            alembic_cfg  = Config()
            alembic_cfg.set_main_option('script_location', "migration/")
            alembic_cfg.set_main_option('sqlalchemy.url', "postgresql+psycopg2://valentine_user:valentine_password@db/valentine_db")
            command.upgrade(alembic_cfg, 'head')
            with cls.session() as session:
                insert_compliments(session)
            