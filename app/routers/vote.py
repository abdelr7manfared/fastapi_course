from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from .. import database,schemes,models,utils,oauth2
from sqlalchemy.orm import Session

router = APIRouter(prefix='/vote',tags=['vote'])
@router.post("/",status_code=status.HTTP_201_CREATED)
def vote(vote:schemes.VoteRequest,db:Session = Depends(database.get_db),current_user : int = Depends(oauth2.get_current_user)):
    post_check = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if post_check is None:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="post not exist")
    
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id ,models.Vote.user_id == current_user.id)
    if vote.dir == True:
    
        if vote_query.first() is not None:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail="you already do vote")
        new_vote = models.Vote(post_id=vote.post_id,user_id = current_user.id)    
        db.add(new_vote)
        db.commit()
        db.refresh(new_vote)
        return {"msg":"up-done"}
    else:
        if vote_query.first() is None:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="you already do vote")
        new_vote = models.Vote(post_id=vote.post_id,user_id = current_user.id)    
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"msg":"delete done"}
