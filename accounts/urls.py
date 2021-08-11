import string

from fastapi import APIRouter
from fastapi import Depends, HTTPException
from typing import Optional

from fastapi import  Query

from database import SessionLocal
from sqlalchemy.orm import Session
from typing import List

router = APIRouter()

from accounts import views, models, schemas



def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

@router.post("/users/", response_model=schemas.User)
def create_user(user: schemas.UserCreate, db: Session = Depends(get_db)):
    db_user = views.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return views.create_user(db=db, user=user)


@router.get("/users/{user_id}", response_model=schemas.User)
def get_user_by_id(user_id: int, db: Session = Depends(get_db)):
    print("reading one user")
    db_user = views.get_user(db, user_id=user_id)
    if db_user is None:
        raise HTTPException(status_code=404, detail="User not found")
    return db_user


@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = views.get_users(db, skip=skip, limit=limit)
    return users


@router.get("/get_user_by_email/{email}", response_model=schemas.User)
def get_user_by_email2(email: str, db: Session = Depends(get_db)):
    print("here man")
    print("email url",email)
    users = views.get_user_by_email(db, email=email)
    return users



