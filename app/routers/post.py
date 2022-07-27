from typing import List, Optional

from fastapi import APIRouter, Depends, HTTPException, Response, status
from sqlalchemy import func
from sqlalchemy.orm import Session

from .. import models, oauth2, schemas
from ..database import get_db

router = APIRouter(prefix="/posts", tags=["Posts"])


@router.get("/", response_model=List[schemas.PostOut])
def get_posts(
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
    limit: int = 10,
    skip: int = 0,
    search: Optional[str] = "",
):
    join_result = (
        db.query(
            models.Post, func.count(models.Votes.posts_id).label("number of votes")
        )
        .join(models.Votes, models.Votes.posts_id == models.Post.posts_id, isouter=True)
        .group_by(models.Post.posts_id)
        .filter(models.Post.title.contains(search))
        .limit(limit)
        .offset(skip)
        .all()
    )
    return join_result


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.Post)
def create_posts(
    post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    new_post = models.Post(
        owner_id=current_user.users_id, **post.dict()
    )  # **post.dict to convert to dict
    db.add(new_post)
    db.commit()
    db.refresh(new_post)
    return new_post


@router.get("/{id_}", response_model=schemas.PostOut)
def get_post(
    id_: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    filter_result = (
        db.query(
            models.Post, func.count(models.Votes.posts_id).label("number of votes")
        )
        .join(models.Votes, models.Votes.posts_id == models.Post.posts_id, isouter=True)
        .group_by(models.Post.posts_id)
        .filter(models.Post.posts_id == id_)
    )
    single_get_post = filter_result.first()
    if not single_get_post:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_} not found",
        )
    return single_get_post


@router.delete("/{id_}", status_code=status.HTTP_204_NO_CONTENT)
def delete_post(
    id_: int,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.posts_id == id_)
    post_to_be_deleted = post_query.first()
    if post_to_be_deleted is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_} does not exist",
        )
    if post_to_be_deleted.owner_id != current_user.users_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action",
        )
    post_query.delete(synchronize_session=False)
    db.commit()
    return Response(status_code=status.HTTP_204_NO_CONTENT)


@router.put("/{id_}", response_model=schemas.Post)
def update_post(
    id_: int,
    updated_post: schemas.PostCreate,
    db: Session = Depends(get_db),
    current_user: int = Depends(oauth2.get_current_user),
):
    post_query = db.query(models.Post).filter(models.Post.posts_id == id_)
    post_to_be_updated = post_query.first()
    if post_to_be_updated is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"post with id: {id_} does not exist",
        )
    if post_to_be_updated.owner_id != current_user.users_id:
        raise HTTPException(
            status_code=status.HTTP_403_FORBIDDEN,
            detail="Not authorized to perform action",
        )
    post_query.update(updated_post.dict(), synchronize_session=False)
    db.commit()
    return post_to_be_updated
