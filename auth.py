from datetime import datetime, timedelta
from typing import Optional
from  accounts.models import User
from passlib.hash import pbkdf2_sha256
from accounts.views import get_user_by_email
from accounts.schemas import TokenData,Token,UserSchema,UserSchema2
from fastapi import Depends, FastAPI, HTTPException, status, APIRouter
from fastapi.security import OAuth2PasswordBearer,OAuth2AuthorizationCodeBearer
from depends import OAuth2PasswordRequestForm
from jose import JWTError, jwt
from passlib.context import CryptContext
from pydantic import  ValidationError
from fastapi.security import (
    OAuth2PasswordBearer,
    SecurityScopes,
)

from database import SessionLocal

ACCESS_TOKEN_EXPIRE_MINUTES = 800
ALGORITHM = "HS256"
from sqlalchemy.orm import Session

SECRET_KEY = "70d05ae34b986bb08a24404e133f01242889c16712a296d339382c2007870fc1"





pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

oauth2_scheme = OAuth2PasswordBearer(tokenUrl="token")

router = APIRouter()

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def verify_password(plain_password, hashed_password):
    print(plain_password,hashed_password)
    return pbkdf2_sha256.verify(plain_password, hashed_password)


def get_password_hash(password):
    return pwd_context.hash(password)


def get_user(db, email: str):
    print(email)
    if email in db:
        user_dict = db[email]
        return UserSchema2(**user_dict)


def authenticate_user(fake_db, email: str, password: str):
    user = get_user(fake_db, email)
    if not user:
        return False
    if not verify_password(password, user.hashed_password):
        return False
    return user


def create_access_token(data: dict, expires_delta: Optional[timedelta] = None):
    to_encode = data.copy()
    if expires_delta:
        expire = datetime.utcnow() + expires_delta
    else:
        expire = datetime.utcnow() + timedelta(minutes=15)
    to_encode.update({"exp": expire})
    encoded_jwt = jwt.encode(to_encode, SECRET_KEY, algorithm=ALGORITHM)
    return encoded_jwt


async def get_current_user(
    security_scopes: SecurityScopes, token: str = Depends(oauth2_scheme),    db: Session = Depends(get_db)

):
    if security_scopes.scopes:
        authenticate_value = f'Bearer scope="{security_scopes.scope_str}"'
    else:
        authenticate_value = f"Bearer"
    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": authenticate_value},
    )
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        email: str = payload.get("sub")
        if email is None:
            raise credentials_exception
        token_scopes = payload.get("scopes", [])
        print(token_scopes)
        token_data = TokenData(scopes=token_scopes, email=email)
    except (JWTError, ValidationError):
        raise
    print("token email here ",token_data.email)
    user = get_user_by_email(db,email=token_data.email)
    if user is None:
        raise credentials_exception
    for scope in security_scopes.scopes:
        if scope not in token_data.scopes:

            raise HTTPException(
                status_code=status.HTTP_401_UNAUTHORIZED,
                detail="Not enough permissions",
                headers={"WWW-Authenticate": authenticate_value},
            )
    return user


async def get_current_active_user(current_user: UserSchema2 = Depends(get_current_user),scopes=["me"]):
    print("current here")
    if current_user.is_active == True:
        raise HTTPException(status_code=400, detail="Inactive user")

    return current_user


# router.post("/token2",response_model=Token)
# async def login2()

@router.post("/token", response_model=Token)
async def login_for_access_token(form_data: OAuth2PasswordRequestForm = Depends(), db:Session = Depends(get_db)):
    print(form_data)
    if form_data.username != "":
        user = get_user_by_email(db,form_data.username)

    else:
        user = get_user_by_email(db,form_data.email)



    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )
    if not verify_password(form_data.password, user.hashed_password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Incorrect email or password",
            headers={"WWW-Authenticate": "Bearer"},
        )

    access_token_expires = timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    access_token = create_access_token(
        data={"sub": user.email, "scopes": "you cant do anything"},
        expires_delta=access_token_expires,
    )
    return {"access_token": access_token, "token_type": "bearer"}


@router.get("/users/me/", response_model=UserSchema2)
async def read_users_me(current_user: UserSchema2 = Depends(get_current_active_user)):

    return current_user

