from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

import os


load_dotenv()

user = os.getenv('user')
pwd = os.getenv('pwd')

SQLALCHEMY_DATABASE_URL = "postgresql://{0}:{1}@db:5432/fast_api".format(user,pwd)

engine = create_engine(
    SQLALCHEMY_DATABASE_URL
)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
