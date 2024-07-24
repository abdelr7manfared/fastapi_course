from fastapi import HTTPException,status,Depends
import jwt
from jwt.exceptions import InvalidTokenError
from datetime import datetime,timedelta
from . import schemes,models
from .database import get_db
from sqlalchemy.orm import Session
from .config import setting
from fastapi.security import OAuth2PasswordBearer
SECRET_KEY = setting.secret_key
ALGORITHM = setting.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = setting.access_token_expire_minutes
oauth_scheme = OAuth2PasswordBearer(tokenUrl='/login')

def create_access_token(data : dict):
    encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    encode.update({"exp":expire})
    return jwt.encode(encode,SECRET_KEY,algorithm=ALGORITHM)
    
def verify_access_token(token:str,credentials_exception):
    try:
        payload = jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])
        id : int = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemes.TokenData(id=id)
    except InvalidTokenError:
        raise credentials_exception
    return token_data
    
    


def get_current_user(token:str = Depends(oauth_scheme) , db:Session = Depends(get_db)):
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )
    new_token = verify_access_token(token,credentials_exception)
    current_user = db.query(models.USer).filter(models.USer.id == new_token.id).first()
    
    return current_user
        
