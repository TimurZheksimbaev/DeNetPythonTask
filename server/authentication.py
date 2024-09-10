from fastapi import Depends, HTTPException
from fastapi.security import HTTPBasic, HTTPBasicCredentials
from sqlalchemy.orm import Session
from passlib.context import CryptContext
from database import get_db
from models import User

# Initialize HTTPBasic and password hashing context
security = HTTPBasic()
pwd_context = CryptContext(schemes=["bcrypt"])


# Utility function to hash passwords
def hash_password(password: str):
    return pwd_context.hash(password)


# Utility function to verify passwords
def verify_password(plain_password: str, hashed_password: str):
    return pwd_context.verify(plain_password, hashed_password)


# Register a new user
def register_user(username: str, password: str, db: Session):
    # Check if the user already exists
    user = db.query(User).filter(User.username == username).first()
    if user:
        raise HTTPException(status_code=400, detail="User already registered")

    # Hash the password and create a new user
    hashed_password = hash_password(password)
    new_user = User(username=username, hashed_password=hashed_password)

    db.add(new_user)
    db.commit()
    db.refresh(new_user)

    return {"message": f"User {username} registered successfully"}


# Authenticate users
def authenticate(credentials: HTTPBasicCredentials = Depends(security), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.username == credentials.username).first()
    if not user or not verify_password(credentials.password, user.hashed_password):
        raise HTTPException(status_code=401, detail="Invalid credentials", headers={"WWW-Authenticate": "Basic"})
    return user.username
