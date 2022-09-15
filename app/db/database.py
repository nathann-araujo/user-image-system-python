from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
import os
DATABASE = os.environ['POSTGRES_NAME']
USERNAME = os.environ['POSTGRES_USER']
PASSWORD = os.environ['POSTGRES_PASSWORD']


SQLALCHEMY_DATABASE_URL = f"postgresql://{USERNAME}:{PASSWORD}@db:5432/{DATABASE}"
engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()


def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()