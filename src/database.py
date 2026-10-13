from sqlalchemy.orm import declarative_base
from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
import os
from dotenv import load_dotenv

#create a session and Base class to get models started

load_dotenv()
db_url = os.getenv("DATABASE_URL")
if db_url is None:
    raise ValueError("DATABASE_URL is missing. Check your .env file.")

engine = create_engine(db_url, echo=True)
Base = declarative_base()
SessionLocal = sessionmaker(autoflush=False, autocommit=False, bind=engine)

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

#Session = sessionmaker(bind=engine)
#session = Session()