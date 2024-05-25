from fastapi import APIRouter,Depends,status,HTTPException
from fastapi.security.oauth2 import OAuth2PasswordRequestForm
from .. import models,schemas
from ..utils import hash_password
from ..database import get_db
from sqlalchemy.orm import Session 



router = APIRouter(
    prefix=
    "/users",
    tags=['Users']
)


@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.UserResponse)
def create_user(user:schemas.UserCreate,db:Session = Depends(get_db)):
    #hashing the password first-the function that hashes is in the utils.py file
    hashed_password = hash_password(user.password)
    #Updates the password with the hashed one in the pydantic model
    user.password= hashed_password
    #creating the user
    new_user = models.User(**user.dict())
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    
    return new_user

@router.get('/{id}',response_model=schemas.UserResponse)
def get_user(id:int,db:Session = (Depends(get_db))):
    user = db.query(models.User).filter(models.User.id == id).first()
    if not user:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="user not found")
    return user
    