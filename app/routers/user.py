from fastapi import APIRouter, Depends, HTTPException, status
from sqlalchemy.orm import Session

from .. import models, schemas, utils
from ..database import get_db

router = APIRouter(prefix="/users", tags=["Users"])


@router.post("/", status_code=status.HTTP_201_CREATED, response_model=schemas.UserOut)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    # hash the password - user.password
    hashed_password = utils.hash(user.password)
    user.password = hashed_password
    new_user = models.User(**user.dict())  # **user.dict to convert to dict
    db.add(new_user)
    db.commit()
    db.refresh(new_user)
    return new_user


# retrieve specific information about a user
@router.get("/{id_}", response_model=schemas.UserOut)
def get_user(id_: int, db: Session = Depends(get_db)):
    user = db.query(models.User).filter(models.User.users_id == id_).first()
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"User with id: {id_} does not exist",
        )
    return user
