from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

URL_DATABASE = "postgresql://postgres:123456@localhost:5432/postgres"

engine = create_engine(URL_DATABASE)
session_local = sessionmaker(bind=engine)
Base = declarative_base()
