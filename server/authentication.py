from typing import Dict

from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy import Column
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models import User

# Basic authentication and hashing algorithm
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"])

# FUcntion for hashing password
def hash_password(password: str) -> str:
    """Hash password
        Parameters
        ----------
        password : str
            password to hash

        Returns
        -------
        str
            hashed password
    """
    return pwd_context.hash(password)


# FUnction for checking password
def verify_password(plain_password: str, hashed_password: str) -> bool:
    """Verify password
        Parameters
        ----------
        plain_password : str
            password which came from user
        hashed_password : str
            password which is stored in database with user's username

        Returns
        -------
        bool
            True if password is correct, otherwise False
    """
    return pwd_context.verify(plain_password, hashed_password)


# Authentication function
def register_user(username: str, password: str, db: Session) -> Dict[str, str]:
    """Register user ( creating a new user)
        Parameters
        ----------
        username : str
            user's name
        password : str
            user's password

        Returns
        -------
        Dict[str, str]
            message that user created successfully

        Raises
        ------
        HTTPException
            If user already exists
    """

    # Check if user already exists
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Hash password and create a new user
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)

    # add user to database
    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User {username} registered successfully"}


def authenticate(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)) -> Column[str]:
    """Аутентификация пользователя базовым методом
        Returns
        -------
        Column[str]
            username
    """
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return user.username
