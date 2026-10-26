from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from typing import List
from sqlalchemy.orm import Session
from .. import models, schemas, utils, oauth2
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    tags=['Authentication']
)
@router.post('/login', response_model=schemas.Token)
# def login(user_credentials: schemas.UserLogin, db: Session = Depends(get_db)):
#     user = db.query(models.User).filter(models.User.email == user_credentials.email).first()
#having fastapi automaticaly get the kews username and password
#it stores as username and password
def login(user_credentials: OAuth2PasswordRequestForm = Depends(), db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=F"Invalid Credentials")

    if not utils.verify(user_credentials.password, user.password):
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail=F"Invalid Credentials")
    #creating a JWT token
    access_token = oauth2.create_access_token(data = {"user_id": user.id})
    #returning a token
    return {"access_token" : access_token, "token_type": "bearer"}

