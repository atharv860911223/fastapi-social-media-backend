from fastapi import FastAPI, Response, status, HTTPException, Depends, APIRouter
from typing import List, Optional
# import os
# from dotenv import load_dotenv
# load_dotenv()
#import psycopg
#from psycopg.rows import dict_row
from sqlalchemy.orm import Session
from sqlalchemy import func
from .. import models, schemas, oauth2
from ..database import engine, SessionLocal, get_db
router = APIRouter(
    prefix = "/posts",
    tags = ["Posts"]
)

# @app.get("/posts")   
# def get_posts():
#     #sql meathod
#     cursor.execute("""SELECT * FROM posts""")
#     posts = cursor.fetchall()
#     return {'data': posts}

@router.get("/", response_model = List[schemas.PostOut]) 
#                   as posts is a list
def get_posts(db: Session = Depends(get_db), limit: int=10, 
            skip: int=0, search: Optional[str]=""):
    #wihtout votes
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()
    #sqlalchemy uses 
    results = db.query(
    models.Post, 
    func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return results


# @app.post("/posts", status_code=status.HTTP_201_CREATED)
# def create_post(post: Post):
#     cursor.execute("""INSERT INTO posts (title, content, rating) 
#                     VALUES(%s, %s, %s) RETURNING*""",
#                     (post.title, post.content, post.rating)
#     )
#     new_post = cursor.fetchone()
#     conn.commit()
#     return {'data': new_post}


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(post: schemas.PostCreate, db: Session = Depends(get_db),
         current_user: int = Depends(oauth2.get_current_user)):
    # new_post = models.Post(title=post.title, content=post.content, rating=post.rating)
    #better meathod
    new_post = models.Post(owner_id = current_user.id, **post.model_dump())
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


#how will fastapi know option ans option 2 different
#Option2
# @router.get("/posts/latest")
# def get_latest_post():
#     cursor.execute("""SELECT * FROM posts ORDER BY id DESC LIMIT 1""")
#     post = cursor.fetchone()
#     return post

#option1
# @app.get("/posts/{id}")
# #id is of str type
# def get_post(id: int):
#     #as the query is str we need to make the id as str
#     #suppose to be a tuple
#     cursor.execute("""SELECT * from posts WHERE id = %s""", (str(id), ))
#     post = cursor.fetchone()
#     if not post:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
#                             detail= f"post with {id} was now found")
#     return {"post_detail": post}

@router.get("/{id}", response_model=schemas.PostOut)
def get_post(id: int, db: Session = Depends(get_db)):
    # post = db.query(models.Post).filter(models.Post.id == id).first()
    post = db.query(
    models.Post, 
    func.count(models.Vote.post_id).label("votes")
    ).join(
        models.Vote,
        models.Vote.post_id == models.Post.id,
        isouter=True
    ).group_by(models.Post.id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail= f"post with {id} was now found")
    return post


# @app.delete("/posts/{id}", status_code=status.HTTP_204_NO_CONTENT)
# def delete_post(id: int):
    
#     cursor.execute("""DELETE FROM posts WHERE id = %s returning *""", (str(id), ))
#     deleted_post = cursor.fetchone()
#     conn.commit()
#     if deleted_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                             detail=f"post with {id} dosen't exist")
    
#     return Response(status_code=status.HTTP_204_NO_CONTENT)

@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()
    if post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
                            detail=f"post with {id} dosen't exist")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                 detail="Not Authorized to Perform the Requested Action")
    post_query.delete(synchronize_session=False)

    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)

# @app.put("/posts/{id}")
# def update_post(id: int, post: Post):
#     cursor.execute("""UPDATE posts SET title=%s, content=%s, rating= %s WHERE id = %s
#                     RETURNING* """,
#                     (post.title, post.content, post.rating, str(id))
#     )
#     updated_post = cursor.fetchone()
#     conn.commit()
#     if updated_post == None:
#         raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, 
#                         detail=f"post with {id} dosen't exist")
    
#     return {'message': updated_post}

 
@router.put("/{id}", response_model=schemas.Post)
def update_post(id: int, updated_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == id)
    post = post_query.first()

    if post is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id {id} doesn't exist"
        )
    if post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                 detail="Not Authorized to Perform the Requested Action")
    post_query.update(
        updated_post.model_dump(),
        synchronize_session=False
    )
    db.commit()

    return post_query.first()