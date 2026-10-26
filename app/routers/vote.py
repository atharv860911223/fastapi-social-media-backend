from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import Optional, List
from sqlalchemy.orm import Session

from .. import models, schemas, utils, oauth2
from ..database import engine, SessionLocal, get_db

router = APIRouter(
    prefix="/vote",
    tags = ["Vote"]
)
@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(vote: schemas.Vote, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="Post not found")

    query = db.query(models.Vote).filter(
        models.Vote.user_id == current_user.id,
        models.Vote.post_id == vote.post_id
    )
    found_vote = query.first()
    if found_vote:
        query.delete(synchronize_session=False)
        db.commit()
        return {"message": "Vote removed successfully"}
    else:
        new_vote = models.Vote(
            post_id=vote.post_id,
            user_id=current_user.id
        )
        db.add(new_vote)
        db.commit()
        return {"message": "Vote added successfully"}