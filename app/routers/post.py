from .. import schemes,models,utils,database,oauth2
from sqlalchemy import func
from sqlalchemy.orm import Session
from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from typing import List

router = APIRouter(prefix="/posts",tags=['posts'])
@router.get("/",response_model=List[schemes.Post_voteResponse])
# @router.get("/")
def get_posts(db:Session = Depends(database.get_db),limit:int = 10 , offset:int=0,search:str=""):
    # posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(offset).all()
    posts = db.query(models.Post,func.count(models.Vote.post_id).label("vote")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).limit(limit).offset(offset).all()
    return posts

@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemes.PostResponse)
def createpost(post : schemes.PostRequest , db:Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    model_user = models.Post(owner_id=current_user.id,**post.dict()) # nice trick 
    db.add(model_user)
    db.commit()
    db.refresh(model_user)
    return model_user

@router.get('/{id}',response_model=schemes.Post_voteResponse)
def get_posts(id:str,db:Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    posts =  db.query(models.Post,func.count(models.Vote.post_id).label("vote")).join(models.Vote,models.Vote.post_id == models.Post.id,isouter=True).group_by(models.Post.id).filter(models.Post.id == id).first()
    # posts = db.query(models.Post).filter(models.Post.id == id).first()
    if posts is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"request post id {id} not found ")  
    if posts.Post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not the post maker")
    return posts

@router.delete('/{id}',status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id : int , db:Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    if posts.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"request post id {id} not found ")  
    if posts.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not the post maker")
    posts.delete(synchronize_session=False)
    db.commit()    
    
@router.put('/{id}',response_model=schemes.PostResponse)
def update_post(id : int  , post:schemes.PostRequest , db:Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    posts = db.query(models.Post).filter(models.Post.id == id)
    if posts.first() is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"request post id {id} not found ")  
    if posts.first().owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"You are not the post maker")
    posts.update(post.dict())
    db.commit()    
    return posts.first()
