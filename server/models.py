from pydantic import BaseModel
from sqlalchemy import Column, Integer, String
from database import Base

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    username = Column(String, unique=True, index=True)
    hashed_password = Column(String)

class UploadResponse(BaseModel):
    message: str
    filename: str
    user: str

# Response model for errors
class ErrorResponse(BaseModel):
    detail: str

class RegisterUserResponse(BaseModel):
    message: str

class RegisterUserRequest(BaseModel):
    username: str
    password: str
