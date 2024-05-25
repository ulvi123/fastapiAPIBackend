from fastapi import APIRouter,Depends,status,HTTPException,Response
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from ..database import get_db
from sqlalchemy.orm import Session
from .. import models,schemas,utils,oauth2
from fastapi.security.oauth2 import OAuth2PasswordRequestForm


router = APIRouter(
    tags=['Auth']
)


@router.post("/login",response_model = schemas.Token)
def login(user_credentials:OAuth2PasswordRequestForm=Depends(), db:Session = Depends(get_db)):
    
    user = db.query(models.User).filter(models.User.email == user_credentials.username).first()
    
    #Checking if the user exists
    if not user:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    #verifying the hashed password of the user in the database and provided plain text password by the user is equal -imported the verify function from the utils.py file
    if not utils.verify(user_credentials.password, user.password): # type: ignore
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,detail="Invalid Credentials")
    
    #create an access token now using the function in the oauth2.py file
    access_token = oauth2.create_access_token(data = {"user_id":user.id})
    
    #returning the access token as a response to the user which will be used to access sensitive data in the database
    return {"access_token":access_token,"token_type":"bearer"}
    