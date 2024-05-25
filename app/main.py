from fastapi import FastAPI 
from . import models 
from .database import engine
from dotenv import load_dotenv 
from app.routers import post,user,auth,vote
from fastapi.middleware.cors import CORSMiddleware


#script that creates models in the postgres when the application runs.It actually checks if the table exists and if not it creates it
models.Base.metadata.create_all(bind=engine)

#Creating the app
app = FastAPI()

origins = [
    "https://www.google.com",
]

#Cors middleware
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins, # type: ignore
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

#Include post and user routers in order the apis work
app.include_router(post.router)
app.include_router(user.router)
app.include_router(auth.router)
app.include_router(vote.router)

# Entry endpoint
@app.get("/")
def root():
    return {"message": "Hello World"}









