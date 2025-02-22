from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker

from .models import Base
from app.config import get_settings

settings = get_settings()
DATABASE_URL = settings.database_url

engine = create_engine(DATABASE_URL, echo=True)

SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def create_database_tables():
    Base.metadata.create_all(bind=engine)
