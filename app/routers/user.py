from ..main import schemes,models,utils
from ..database import get_db
from sqlalchemy.orm import Session
from fastapi import FastAPI,status,HTTPException,Depends,APIRouter
router = APIRouter(prefix="/users",tags=['users'])

@router.post('/',status_code=status.HTTP_201_CREATED,response_model=schemes.UserRespone)
def create_user(user : schemes.UserRequest , db:Session = Depends(get_db)):
    user_exist = db.query(models.USer).filter(models.USer.Email == user.Email).first()
    if user_exist is not None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"email {user.Email} already exist")  
    user.Password = utils.hash(user.Password)
    new_user = models.USer(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user

@router.get('/{id}',response_model=schemes.UserRespone)
def get_user(id : int , db: Session = Depends(get_db)):
    user = db.query(models.USer).filter(models.USer.id == id).first()
    if user is None:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail=f"request post id {id} not found ")  
    return user
