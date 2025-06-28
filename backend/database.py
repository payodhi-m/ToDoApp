import os
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker, declarative_base
from dotenv import load_dotenv

#Loading environment variables from .env
load_dotenv()

#Getting the DB URL from environment
DATABASE_URL = os.getenv("DATABASE_URL")

#Creating engine

engine = create_engine(DATABASE_URL, connect_args={"check_same_thread": False} if "sqlite" in DATABASE_URL else {})

#Creating session
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

#Base class for models
Base = declarative_base()


