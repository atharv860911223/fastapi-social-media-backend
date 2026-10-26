from pydantic import BaseModel, Field, EmailStr
from typing import Optional
from datetime import datetime
#we can have different schemas
class UserCreate(BaseModel):
    email: EmailStr
    password: str 

class UserOut(BaseModel):
    id: int
    email: EmailStr
    created_at: datetime
    #tells the pydantic to convert the orm model into dict
    class Config:
        from_attributes = True

class Vote(BaseModel):
    post_id: int

class PostCreate(BaseModel):
    title: str
    content: str
    rating: Optional[int] = None

class Post(BaseModel):
    title: str
    content: str
    rating: int
    owner_id: int
    owner: UserOut
    #tells the pydantic to convert the orm model into dict
    class Config:
        from_attributes = True

class PostOut(BaseModel):
    Post: Post
    votes: int
    class Config:
        from_attributes = True


class UserLogin(BaseModel):
    email: EmailStr
    password: str 

class Token(BaseModel):
    access_token: str
    token_type: str

class TokenData(BaseModel):
    id: Optional[int] = None


