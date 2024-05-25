from fastapi import APIRouter,Depends,status,HTTPException,Response
from .. import schemas,database,models,oauth2
from ..database import get_db
from sqlalchemy.orm import Session

router = APIRouter(
    prefix=
    "/vote",
    tags=['Vote']
)

@router.post('/',status_code=status.HTTP_201_CREATED)
def vote(vote:schemas.Vote,db:Session = Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # checking if the post exists
    post = db.query(models.Post).filter(models.Post.id == vote.post_id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with id: {vote.post_id} does not exist")
    
    # getting the vote query
    vote_query = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,models.Vote.user_id == current_user.id)
    # checking if the post exists and fetching the first
    found_vote = vote_query.first()
    # if the vote exists then raise an error since user can only vote on post once
    if vote.dir == 1:
        if found_vote:
            raise HTTPException(status_code=status.HTTP_409_CONFLICT,detail=f"user {current_user.id} has already voted on post {vote.post_id}")
        #if not then create a new vote
        new_vote = models.Vote(post_id = vote.post_id,user_id=current_user.id)
        db.add(new_vote)
        db.commit()
        return {"message":"successfully added vote"}
    else:
        #if the vote exists then delete it
        if not found_vote:
            raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail="Vote does not exist")
        #if not then delete the vote
        vote_query.delete(synchronize_session=False)
        # saving the changes
        db.commit()
        # returning a message
        return {"message":"successfully deleted vote"}
        
        
        	

