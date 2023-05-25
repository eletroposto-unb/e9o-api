from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from lib.config.env import settings

SQLALCHEMY_DATABASE_URL = settings.db_connect_url


engine = create_engine(
    SQLALCHEMY_DATABASE_URL,
    pool_size=200,
    max_overflow=0
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

def get_database(expire_on_commit: bool = True):
    db = SessionLocal(expire_on_commit=expire_on_commit)
    try:
        return db
    finally:
        db.close()

def initialize_database():
    Base.metadata.create_all(bind=engine)