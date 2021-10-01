from os import getenv, environ
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

try:
    SQLALCHEMY_DATABASE_URL = getenv('HEROKU_SQL_DB')
    if SQLALCHEMY_DATABASE_URL is None:
        SQLALCHEMY_DATABASE_URL = environ.get('HEROKU_SQL_DB')
except KeyError:
    raise KeyError("Set environment variable 'HEROKU_SQL_DB' to PostgreSQL URL")

# SQLALCHEMY_DATABASE_URL = "sqlite:///./sql_app.db"

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(
    autocommit=False,
    autoflush=False,
    bind=engine
)

Base = declarative_base()
