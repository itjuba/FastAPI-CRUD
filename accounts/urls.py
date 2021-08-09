from fastapi import APIRouter
from fastapi import Depends, HTTPException
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

@router.get("/users/", response_model=List[schemas.User])
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(get_db)):
    users = views.get_users(db, skip=skip, limit=limit)
    return users

