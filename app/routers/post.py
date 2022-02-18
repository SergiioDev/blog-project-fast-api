from typing import List, Optional
from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy import func
from sqlalchemy.orm import Session
from .. import models, schemas, oauth2
from ..database import get_db

router = APIRouter(
    prefix="/posts",
    tags=['Posts']
)


@router.get("/", response_model=List[schemas.PostResponse])
def get_posts(db: Session = Depends(get_db), current_user: models.User = Depends(oauth2.get_current_user),
              limit: int = 10, skip: int = 0, search: Optional[str] = ""):

    posts_with_likes = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(
        models.Post.title.contains(search)).limit(limit).offset(skip).all()

    return posts_with_likes


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.PostResponse)
def create_posts(post: schemas.PostCreate, db: Session = Depends(get_db),
                 curent_user: models.User = Depends(oauth2.get_current_user)):
    post = models.Post(owner_id=curent_user.id, **post.dict())
    db.add(post)
    db.commit()
    db.refresh(post)
    return post


@router.get("/{post_id}", response_model=schemas.PostResponse)
def get_post(post_id: int, db: Session = Depends(get_db),
             curent_user_id: models.User = Depends(oauth2.get_current_user)):

    post = db.query(models.Post, func.count(models.Vote.post_id).label("likes")).join(
        models.Vote, models.Vote.post_id == models.Post.id, isouter=True).group_by(models.Post.id).filter(models.Post.id == post_id).first()

    if not post:
        raise HTTPException(status.HTTP_404_NOT_FOUND, f"post with id {post_id} was not found")

    return post


@router.put("{post_id}", response_model=schemas.PostResponse)
def update_post(post_id: int, post: schemas.PostCreate, db: Session = Depends(get_db),
                curent_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)

    if not post_query.first():
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} does not exists")

    if post_query.owner_id != curent_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you're not the owner of this post")

    post_query.update(post.dict(), synchronize_session=False)

    db.commit()
    return post_query.first()


@router.delete("/{post_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(post_id: int, db: Session = Depends(get_db),
                curent_user: models.User = Depends(oauth2.get_current_user)):
    post_query = db.query(models.Post).filter(models.Post.id == post_id)
    post = post_query.first()

    if not post:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"post with id {post_id} does not exists")

    if post.owner_id != curent_user.id:
        raise HTTPException(status_code=status.HTTP_403_FORBIDDEN, detail="you're not the owner of this post")

    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)
