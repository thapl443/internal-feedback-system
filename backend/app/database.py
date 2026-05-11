from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base
import os

Base = declarative_base()

# 1. Get fundamental DB settings
DB_SCHEMA = os.getenv("DB_SCHEMA", "internal_portal")
DATABASE_URL = os.getenv("DATABASE_URL")

# 2. Construct URL if not provided (Local Dev Fallback)
if not DATABASE_URL:
    DB_HOST = os.getenv("DB_HOST", "localhost")
    DB_USER = os.getenv("POSTGRES_USER", "postgres")
    DB_PASS = os.getenv("POSTGRES_PASSWORD", "password123")
    DB_NAME = os.getenv("POSTGRES_DB", "nexus_portal")
    DB_PORT = os.getenv("DB_PORT", "5432")
    DATABASE_URL = f"postgresql://{DB_USER}:{DB_PASS}@{DB_HOST}:{DB_PORT}/{DB_NAME}"

# 3. Apply Schema configuration (Senior level practice)
Base.metadata.schema = DB_SCHEMA

connect_args = {}
if "postgresql" in DATABASE_URL:
    connect_args["options"] = f"-csearch_path={DB_SCHEMA}"

engine = create_engine(DATABASE_URL, connect_args=connect_args)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
