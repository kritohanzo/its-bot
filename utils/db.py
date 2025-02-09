from contextlib import contextmanager
from os import getenv

from alembic import command
from alembic.config import Config
from dotenv import load_dotenv
from sqlalchemy import create_engine, text
from sqlalchemy.orm import Session


load_dotenv()


DATABASE_URL = f"postgresql+psycopg2://{getenv('POSTGRES_USER')}:{getenv('POSTGRES_PASSWORD')}@{getenv('DB_HOST')}/{getenv('POSTGRES_DB')}"
SCRIPT_LOCATION = 'migrations'
ENGINE = create_engine(url=DATABASE_URL)


class Database:
    @classmethod
    @contextmanager
    def session(cls):
        session = Session(ENGINE)
        yield session
        session.close()

    @classmethod
    def initialize_database(cls):
        alembic_cfg = Config()
        alembic_cfg.set_main_option(name='sqlalchemy.url', value=DATABASE_URL)
        alembic_cfg.set_main_option(name='script_location', value=SCRIPT_LOCATION)
        command.upgrade(alembic_cfg, 'head')

    @classmethod
    def initialize_compliments(cls):
        with cls.session() as session:
            with open('common/compliments.sql') as file:
                for line in file.readlines():
                    query = text(line)
                    session.execute(query)
            session.commit()
