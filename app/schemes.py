
from typing import Optional
from pydantic import BaseModel, Field,EmailStr
from datetime import datetime

from .models import USer

class PostRequest(BaseModel):
    title:str
    content:str
    Publised:bool = Field(default=True)



class UserRequest(BaseModel):
    Email : EmailStr
    username:str
    Password:str
    phone_number:str

class UserRespone(BaseModel):
    id:int
    phone_number:str
    Email : EmailStr
    username:str
    created_at:datetime
    
class PostResponse(PostRequest):
    id:int
    created_at:datetime
    owner_id : int
    owner : UserRespone

class Post_voteResponse(BaseModel):
    Post:PostResponse
    vote:int


class UserLoginRequest(BaseModel):
    Email : EmailStr
    Password:str
    
class TokenData(BaseModel):
    id:Optional[int]=None
    
    
class VoteRequest(BaseModel):
    post_id : int
    dir : bool