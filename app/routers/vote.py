from fastapi import Response, status, HTTPException, Depends, APIRouter
from sqlalchemy.orm import Session

from .. import schemas, database, models, oauth2

router = APIRouter(
    prefix="/like",
    tags=['Like']
)


@router.post("/", status_code=status.HTTP_201_CREATED)
def like_post(vote: schemas.Vote, db: Session = Depends(database.get_db),
              current_user: models.User = Depends(oauth2.get_current_user)):
    check_vote_exists = db.query(models.Vote).filter(models.Vote.post_id == vote.post_id,
                                                     models.Vote.user_id == current_user.id)

    check_post_exists = db.query(models.Post).filter(models.Post.id == vote.post_id).first()

    if not check_post_exists:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=f"Post with id {vote.post_id} doesn't exists")

    if check_vote_exists.first() and vote.dir == 1:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT,
                            detail=f"user {current_user.id} has already voted on post {vote.post_id}")

    created_vote = models.Vote(post_id=vote.post_id, user_id=current_user.id)

    if vote.dir == 0:
        check_vote_exists.delete(synchronize_session=False)
        db.commit()
        return {"message": "Like deleted successfully"}

    if vote.dir == 1:
        db.add(created_vote)
        db.commit()
        return {"message": "Like added successfully"}
