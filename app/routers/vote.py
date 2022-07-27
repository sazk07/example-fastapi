from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import database, models, oauth2, schemas

router = APIRouter(prefix="/vote", tags=["Votes"])


@router.post("/", status_code=status.HTTP_201_CREATED)
def vote(
    vote: schemas.Vote,
    db: Session = Depends(database.get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.posts_id == vote.posts_id)
    grab_post = post_query.first()
    if not grab_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Post with id: {vote.posts_id} does not exist",
        )
    vote_query = db.query(models.Votes).filter(
        models.Votes.posts_id == vote.posts_id,
        models.Votes.users_id == current_user.users_id,
    )
    found_vote = vote_query.first()
    if vote.votes_dir == 1:
        if found_vote:
            raise HTTPException(
                status_code=status.HTTP_409_CONFLICT,
                detail=f"user {current_user.users_id} hs already voted on post {vote.posts_id}",
            )
        new_vote = models.Votes(posts_id=vote.posts_id, users_id=current_user.users_id)
        db.add(new_vote)
        db.commit()
        return {"message": "successfully added vote"}
    else:
        if not found_vote:
            raise HTTPException(
                status_code=status.HTTP_404_NOT_FOUND, detail="Vote does not exist"
            )
        vote_query.delete(synchronize_session=False)
        db.commit()
        return {"message": "successfully deleted vote"}
