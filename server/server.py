from typing import Dict

from fastapi import FastAPI, File, UploadFile, HTTPException, Depends, Form
import os
from authentication import authenticate, register_user
from database import Base, engine, get_db
from models import *
from sqlalchemy.orm import Session

from starlette.responses import FileResponse

app = FastAPI()

Base.metadata.create_all(bind=engine)

UPLOAD_DIR = "./server/uploads"
os.makedirs(UPLOAD_DIR, exist_ok=True)


@app.post("/register", response_model=RegisterUserResponse, responses={
    200: {"message": "Registered user"},
    400: {"model": ErrorResponse, "description": "Bad request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
def register(user: RegisterUserRequest, db: Session = Depends(get_db)) -> Dict[str, str]:
    """ Register user ( creating a new user)
        Parameters
        ----------
        user: RegisterUserRequest
            user's name and password

        Returns
        -------
        Dict[str, str]
            message

        Raises
        ------
        HTTPException
            If user already exists, or failed registration
        """
    try:
        return register_user(user.username, user.password, db)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))



@app.post("/upload", response_model=UploadResponse, responses={
    200: {"description": "File uploaded successfully"},
    400: {"model": ErrorResponse, "description": "Bad request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def upload_file(file: UploadFile = File(...), username: str = Depends(authenticate)) -> Dict[str, str]:
    """ Upload file
        Parameters
        ----------
        file: File
            file to upload

        Returns
        -------
        Dict[str, str]
            UploadResponse message

        Raises
        ------
        HTTPException
            If file upload failed
        """
    file_path = os.path.join(UPLOAD_DIR, file.filename)
    try:
        with open(file_path, "wb") as f:
            while content := await file.read(1024):
                f.write(content)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

    return {"message": "File uploaded successfully", "filename": file.filename, "user": username}



@app.get("/download", responses={
    200: {"description": "File downloaded successfully"},
    400: {"model": ErrorResponse, "description": "Bad request"},
    401: {"model": ErrorResponse, "description": "Unauthorized"},
    404: {"model": ErrorResponse, "description": "File not found"},
    500: {"model": ErrorResponse, "description": "Internal server error"}
})
async def download_file(filename: str, username: str = Depends(authenticate)) -> FileResponse:
    """ Download file
        Parameters
        ----------
        filename: str
            file to download

        Returns
        -------
        FileResponse
            file response

        Raises
        ------
        HTTPException
            If file download failed
        """
    file_path = os.path.join(UPLOAD_DIR, filename)
    if not os.path.exists(file_path):
        raise HTTPException(status_code=404, detail="File not found")

    return FileResponse(file_path, media_type='application/octet-stream', filename=filename)
