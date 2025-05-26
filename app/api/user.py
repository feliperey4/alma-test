"""
Written by Felipe Rey
"""
from datetime import timedelta

from fastapi import APIRouter, Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jose import jwt, JWTError
from pydantic import BaseModel
from sqlalchemy.orm import Session

from app.config import ACCESS_TOKEN_EXPIRE_MINUTES, AUTH_SECRET_KEY, AUTH_ALGORITHM
from app.database import get_db
from app.service.user_service import AuthService

user_route = APIRouter(tags=['Internal Authentication'])

class UserData(BaseModel):
    username: str
    password: str

class Token(BaseModel):
    access_token: str


@user_route.post("/internal/auth/register", status_code=204)
def register(user: UserData, db: Session = Depends(get_db)):
    """
    Register a new user (Attorney internal user).
    """
    db_user = AuthService.get_user(db, user.username)
    if db_user:
        raise HTTPException(status_code=400, detail="Username already registered")
    _ = AuthService.create_user(db, user.username, user.password)



@user_route.post("/internal/auth/login", response_model=Token)
async def login(user_credentials: UserData, db: Session = Depends(get_db)):
    """
    Login using internal user and password.
    """
    user = AuthService.authenticate_user(db, user_credentials.username, user_credentials.password)
    if not user:
        raise HTTPException(
            status_code=401,
            detail="Incorrect username or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = AuthService.create_access_token(
        data={"sub": user.username}, expires_delta=access_token_expires
    )
    return {"access_token": access_token}


# auth validation

security = HTTPBearer()

async def get_current_user(
        credentials: HTTPAuthorizationCredentials = Depends(security),
        db: Session = Depends(get_db)
):
    """
    Validate JWT token.
    """
    credentials_exception = HTTPException(
        status_code=401,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    try:
        payload = jwt.decode(credentials.credentials, AUTH_SECRET_KEY, algorithms=[AUTH_ALGORITHM])
        username: str = payload.get("sub")
        if username is None:
            raise credentials_exception
    except JWTError:
        raise credentials_exception

    user = AuthService.get_user(db, username)
    if user is None:
        raise credentials_exception
    return user