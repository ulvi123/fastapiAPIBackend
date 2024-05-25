from jose import JWTError, jwt
from datetime import datetime, timedelta
from . import schemas,database
from fastapi import Depends, status, HTTPException
from . import oauth2
from fastapi.security import OAuth2PasswordBearer
from sqlalchemy.orm import Session
from . import models
from .config import settings


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

#SECRET_KEY 
#ALGORITHM
#EXPIRATION_TIME

SECRET_KEY = settings.secret_key
ALGORITHM = settings.algorithm
ACCESS_TOKEN_EXPIRE_MINUTES = settings.access_token_expire_minutes


def create_access_token(data: dict):
    to_encode = data.copy()
    expire = datetime.utcnow() + timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES) 
    to_encode.update({"exp": expire})
    encoded_jwt_token = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM) # type: ignore
    return encoded_jwt_token

def verify_access_token(token:str,credentials_exception):
    try:
        payload=jwt.decode(token,SECRET_KEY,algorithms=[ALGORITHM])#type: ignore
        id = payload.get("user_id")
        if id is None:
            raise credentials_exception
        token_data = schemas.TokenData(id=str(id)) #here extracted id from token should be converted to string in order the schema validation of TokenData to work
    except JWTError:
        raise credentials_exception
    
    return token_data #it is actually the extracted from the user request and  which will be returned to the user requesting an access to any endpoint.The result is either user can or cannot access the endpoint in the post.py file for example.
    
#every time there is a protected route the request should run through the below function to identify if the user is authenticated. And next the verify_access_token function is called with the token being extracted from the header of the request.
def get_current_user(token: str = Depends(oauth2_scheme),db:Session = Depends(database.get_db)):
    credentials_exception = HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="Could not validate credentials", headers={"WWW-Authenticate": "Bearer"})
    
    #here we get the returned token that we receive back from the verify_access_token function
    token = verify_access_token(token, credentials_exception) # type: ignore
    
    #we can make query to the database and get the user from there base on the extracted id from the token
    user = db.query(models.User).filter(models.User.id == token.id).first() # type: ignore
    
    return user

