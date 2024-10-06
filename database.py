import os
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

# Load environment variables from .env file
load_dotenv()

# Debug print to check if DB_URL is loaded
print(f"DB_URL from .env: {os.getenv('DB_URL')}")

# Get the database URL from environment variables
SQLALCHEMY_DATABASE_URL = os.getenv("DB_URL")

if SQLALCHEMY_DATABASE_URL is None:
    raise ValueError("DB_URL environment variable is not set or .env file not loaded")

engine = create_engine(SQLALCHEMY_DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()
