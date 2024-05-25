from pydantic import BaseModel,Field
from datetime import datetime
from pydantic import EmailStr,conint
from typing import Optional

#How the response should look like
#User related pydantic schemas
#Request model
class UserCreate(BaseModel):
    email: EmailStr
    password: str
    
#Response model    
class UserResponse(BaseModel):
    id:int
    email:EmailStr
    created_at:datetime
    class Config:
        orm_mode = True
        
        
        
#How the requests should look like from the client- this section is for posts table in the database-everything we define here is related to posts

class Post(BaseModel):
    title: str = Field(default=..., min_length=3, max_length=20)
    content: str = Field(default=..., min_length=10, max_length=250)
    published:bool = Field(default=True)
    
class PostBase(BaseModel):
    title: str
    content: str
    published:bool = True
    
class PostCreate(PostBase):
    pass

class PostUpdate(PostBase):
    pass


#How the responses for Post model should look like from the server/ also we inherit from postbase so no need for the 3 fields to be mentioned(title,content,published)
class PostResponse(PostBase):
    id:int
    created_at:datetime
    owner_id: int
    owner: UserResponse #using another pydantic model
    class Config:
        orm_mode = True
  
class PostOut(BaseModel):
    Post: PostResponse
    votes: int
        
        


#AUth related schemas
#Login
class UserLogin(BaseModel):
    email: EmailStr
    password: str
    
#schema for token
class Token(BaseModel):
    access_token: str
    token_type: str
    
class TokenData(BaseModel):
    id: str
    
    
class Vote(BaseModel):
    post_id: int
    dir: int # type: ignore
    
    
