from sqlalchemy import create_engine, Column, Integer, String
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

# a simple sqlite database
DATABASE_URL = "sqlite:///./server/test.db"

# create a database engine
engine = create_engine(DATABASE_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)
Base = declarative_base()

# Get database session
def get_db():
    """Get database session
        Returns
        -------
            database session
    """
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()
