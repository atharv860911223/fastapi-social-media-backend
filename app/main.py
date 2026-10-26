#CRUD application
# Create - POST - /post
# to get all the post or one of the post
# Read - GET, GET - /post/:id, /post respectively
# Update -PUT/PATCH - /post/:id
#difference between put and patch
# PUT - change the entire things
# PATCH - only change the one field on a pust 
# we will have to send the id for both
# Delete -DELETE- /post/:id
# 
#@app._______/post/{id})
#get is the meathod
from fastapi import FastAPI, Response, status, HTTPException, Depends
from typing import Optional, List
import os
from dotenv import load_dotenv
load_dotenv()
import psycopg
from psycopg.rows import dict_row

from sqlalchemy.orm import Session

from . import models, schemas, utils
from .database import engine, SessionLocal, get_db
from .routers import user, post, auth, vote
from fastapi.middleware.cors import CORSMiddleware
#as alembic cam=n directy create every thing by alembic revision --autogenerate -m""
#models.Base.metadata.create_all(bind=engine)

app = FastAPI()
#to set a public api do * 
origins = ["*"]

app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

@app.get("/")
def test_post(db: Session = Depends(get_db)):
    return {"status":"success"}

app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)