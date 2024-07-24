from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
from sqlalchemy.orm import Session
from .. import database ,schemes,models,utils,oauth2
router = APIRouter(tags=['Authentication'])
@router.post('/login')
def login(user:schemes.UserLoginRequest,db:Session = Depends(database.get_db)):
    user_exist = db.query(models.USer).filter(models.USer.Email == user.Email).first()
    if user_exist is None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Invalid credentials")
    # check Password 
    if not utils.verfiy(user.Password,user_exist.Password):
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"Wrong Password")
    
    accessToken = oauth2.create_access_token(data={"user_id":user_exist.id})
    
    return {"Token":accessToken}
          
    

    
    