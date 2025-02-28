from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from dotenv import load_dotenv

load_dotenv()
import os
# DB_URL = DB_URL = os.getenv("DB_URL")
DB_URL = "sqlite:///./sql_app.db"
engine = create_engine(DB_URL,echo=True)
SessionLocal = sessionmaker(autocommit=False,autoflush=False, bind=engine)

Base = declarative_base()


# Database cursor !!
def get_db():
    db = SessionLocal()
    try : 
        yield db
    finally:
        db.close()
        