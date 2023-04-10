from fastapi import Response, status, HTTPException, Depends, APIRouter
from app import models
from app.database import get_db
from sqlalchemy.orm import Session
from sqlalchemy import func
from typing import List, Optional
import app.schemas as schemas
import app.oauth2 as oauth2

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostOut])
# @router.get("/")
async def get_posts(db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user), limit: int = 10, skip: int = 0, search: Optional[str] = ""):
    # cursor.execute("""SELECT * FROM posts """)
    # posts = cursor.fetchall()
    # posts = db.query(models.Post).all()

    #posts = db.query(models.Post).filter(models.Post.title.contains(
    #    search)).limit(limit=limit).offset(offset=skip).all()
    
    results = db.query(models.Post, func.count(models.Vote.post_id).label("votes")).join(models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.title.contains(search)).limit(limit=limit).offset(offset=skip).all()
    
    return results


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_post(new_post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):

    # cursor.execute("""INSERT INTO posts (title,content,published) VALUES (%s,%s,%s) RETURNING * """,
    #               (new_post.title, new_post.content, new_post.published))
    # created_post = cursor.fetchone()
    # conn.commit()

    # post_dict = new_post.dict()
    # post_dict['id'] = randrange(0,100000)
    # my_posts.append(post_dict)
    print(current_user.id)
    created_post = models.Post(owner_id=current_user.id, **new_post.dict())
    # title=new_post.title,content=new_post.content,published=new_post.published)
    db.add(created_post)
    db.commit()
    db.refresh(created_post)
    return created_post


@router.get("/{id}", response_model=schemas.Post)
async def get_post(id: int, response: Response, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""SELECT * FROM posts WHERE id = %s """, str(id))
    # post = cursor.fetchone()

    post = db.query(models.Post).filter(models.Post.id == id).first()
    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} not found")
        # response.status_code = status.HTTP_404_NOT_FOUND
        # return {'message':f"post with {id} not found"}

    return post


@router.delete("/{id}", status_code=status.HTTP_204_NO_CONTENT)
async def delete_post(id: int, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""DELETE FROM posts WHERE id = %s RETURNING * """, str(id))
    # deleted_post = cursor.fetchone()
    # conn.commit()
    deleted_post_query = db.query(models.Post).filter(models.Post.id == id)
    deleted_post = deleted_post_query.first()
    if deleted_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    if deleted_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    deleted_post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id}", response_model=schemas.Post)
async def update_post(id: int, post: schemas.PostCreate, db: Session = Depends(get_db), current_user: int = Depends(oauth2.get_current_user)):
    # cursor.execute("""UPDATE posts SET title = %s,content = %s,published = %s WHERE id = %s RETURNING * """,
    #               (post.title, post.content, post.published, str(id)))
    # updated_post = cursor.fetchone()
    # conn.commit()
    update_query = db.query(models.Post).filter(models.Post.id == id)
    updated_post = update_query.first()

    if updated_post == None:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND,
                            detail=f"post with {id} does not exist")
    if updated_post.owner_id != current_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN,
                            detail="Not authorized to perform requested action")
    update_query.update(post.dict(), synchronize_session=False)
    db.commit()
    return update_query.first()
