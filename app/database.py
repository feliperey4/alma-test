"""
Written by Felipe Rey
"""
import enum
from datetime import datetime

from sqlalchemy import create_engine, DateTime
from sqlalchemy import Column, Integer, String, LargeBinary, Enum
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker

from app.config import DB_URL

engine = create_engine(DB_URL)
SessionLocal = sessionmaker(autocommit=False, autoflush=False, bind=engine)

Base = declarative_base()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


# models
class LeadState(enum.Enum):
    PENDING = "PENDING"
    REACHED_OUT = "REACHED_OUT"


class Lead(Base):
    __tablename__ = "leads"

    id = Column(Integer, primary_key=True, index=True, autoincrement=True)
    email = Column(String, nullable=False, index=True)
    f_name = Column(String, nullable=False)
    l_name = Column(String, nullable=False)
    cv_name = Column(String, nullable=False)
    state = Column(Enum(LeadState), default=LeadState.PENDING)
    cv_content = Column(LargeBinary, nullable=False)


class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String(50), unique=True, index=True)
    hashed_password = Column(String(255))
    created_at = Column(DateTime, default=datetime.utcnow)
