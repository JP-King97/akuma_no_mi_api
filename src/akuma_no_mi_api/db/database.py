from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

SQLALCHEMY_DATABASE_URL="postgresql://postgres:Jp3141592@localhost:5432/one_piece_db"
engine = create_engine(SQLALCHEMY_DATABASE_URL, echo=True)
SessionLocal = sessionmaker(bind = engine, autocommit = False, autoflush = False)
Base = declarative_base()

def get_db():

    db = SessionLocal() 
    try:
        yield db
    finally:
        db.close()