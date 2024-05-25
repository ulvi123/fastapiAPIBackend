from fastapi import APIRouter,Depends,status,HTTPException,Response
from typing import Optional,List
from .. import models,schemas # type: ignore
from sqlalchemy.orm import Session 
from ..database import get_db  # type: ignore
from .. import oauth2
from sqlalchemy import func


router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/",response_model = List[schemas.PostOut])
def get_posts(db:Session = Depends(get_db),current_user:int = Depends(oauth2.get_current_user),
              limit = 1,skip = 0,search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts""")
    # posts = cursor.fetchall()
    
    #this query queries the database and return the result of the query
    posts = db.query(models.Post).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all() 
    return posts
    
    # this query joins two tables and returns the count of votes for each post
    # results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit).offset(skip).all()

    # return results

#here get_current_user function is called from oauth2.py file to identify if the user can access the route.Its purpose is to ensure that the user trying to access the route is authenticated.Currently we return user from the oauth2.py file's get_current_user function and it is stored in the current_user variable
@router.post("/",status_code=status.HTTP_201_CREATED,response_model=schemas.PostResponse)
def create_posts(post:schemas.PostCreate, db:Session = (Depends(get_db)), current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING *""",
    #                (post.title,post.content,post.published)) # type: ignore
    # new_post = cursor.fetchone()
    # conn.commit()
    print(current_user.id)
    new_post = models.Post(owner_id = current_user.id,**post.dict()) #create - can be used as *post.dict() to set default values when there are too many model values
    db.add(new_post) #add to db
    db.commit() #commit to db
    db.refresh(new_post) #refresh to db
    return new_post

@router.get('/{id}',response_model=schemas.PostOut)
def get_post(id:int,db:Session=(Depends(get_db)),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s""",(str(id),))
    # post = cursor.fetchone()
    # if not post:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"post with the id of {id} was not found")
    
    single_post = db.query(models.Post).filter(models.Post.id == id).first()
    # results = db.query(models.Post,func.count(models.Vote.post_id).label("votes")).join(models.Vote,models.Vote.post_id == models.Post.id, isouter = True).group_by(models.Post.id).filter(models.Post.id == id).first()
    
    if not single_post:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="post not found")
    return single_post

    # return results


@router.delete("/{id}",status_code=status.HTTP_204_NO_CONTENT)
def delete_post(id:int,db:Session = (Depends(get_db)),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s returning *""",(str(id),)) # type: ignore
    # deleted_post = cursor.fetchone()
    # if deleted_post == None:
    #     raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,detail=f"the post with the id of {id} was not found")
    # conn.commit()
    
    # querying the post we wanna delete
    post = db.query(models.Post).filter(models.Post.id == id).first()
    # checking if the post exists
    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="post not found")
    # checking if the user is authorized to delete the post
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="not authorized to perform requested action")
    # deleting the post   
    db.delete(post)
    # saving the changes
    db.commit()
    # return the deleted post
    return Response(status_code=status.HTTP_204_NO_CONTENT) # type: ignore



@router.put("/{id}",response_model=schemas.PostResponse)
def update_post(id:int,updated_post:schemas.PostUpdate,db:Session=Depends(get_db),current_user = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title= %s, content = %s,published = %s WHERE id = %s RETURNING *""",
    #                (post.title, post.content, post.published,str(id))) # type: ignore
    
    # updated_post = cursor.fetchone()

    # if updated_post == None:
    #     raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="updated post not found")
    
    # conn.commit()
    
    post_query= db.query(models.Post).filter(models.Post.id == id)
    
    post = post_query.first()

    if post == None:
        raise HTTPException(status_code = status.HTTP_404_NOT_FOUND,detail="post not found")
    if post.owner_id != current_user.id:
        raise HTTPException(status_code = status.HTTP_403_FORBIDDEN,detail="not authorized to perform requested action")
    post_query.update(updated_post.dict(),synchronize_session=False) # type: ignore
    db.commit()    
    return post_query.first()	#returning the updated post	