"""
Written by Felipe Rey
"""
from datetime import timedelta, datetime
from typing import *

from jose import jwt, JWTError
from passlib.context import CryptContext
from sqlalchemy.orm import Session

from app.config import AUTH_SECRET_KEY, AUTH_ALGORITHM
from app.database import User



class AuthService:
    PWD_CONTEXT = CryptContext(schemes=["bcrypt"], deprecated="auto")

    @classmethod
    def get_user(cls, db: Session, username: str) -> Optional[User]:
        return db.query(User).filter(User.username == username).first()

    @classmethod
    def authenticate_user(cls, db: Session, username: str, password: str) -> Optional[
        User]:
        user = cls.get_user(db, username)
        if not user:
            return None
        if not cls.PWD_CONTEXT.verify(password, user.hashed_password):
            return None
        return user

    @classmethod
    def create_access_token(cls, data: dict, expires_delta: Optional[timedelta] = None):
        to_encode = data.copy()
        if expires_delta:
            expire = datetime.utcnow() + expires_delta
        else:
            expire = datetime.utcnow() + timedelta(minutes=15)
        to_encode.update({"exp": expire})
        encoded_jwt = jwt.encode(to_encode, AUTH_SECRET_KEY, algorithm=AUTH_ALGORITHM)
        return encoded_jwt

    @classmethod
    def create_user(cls, db: Session, username: str, password: str) -> User:
        hashed_password = cls.PWD_CONTEXT.hash(password)
        db_user = User(
            username=username,
            hashed_password=hashed_password
        )
        db.add(db_user)
        db.commit()
        db.refresh(db_user)
        return db_user

