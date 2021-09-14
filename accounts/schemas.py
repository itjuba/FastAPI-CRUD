from typing import List, Optional

from pydantic import BaseModel


class Token(BaseModel):
    access_token: str
    token_type: str


class TokenData(BaseModel):
    email: Optional[str] = None


class UserSchema2(BaseModel):
    id: int
    email: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True



class UserSchema3(BaseModel):
    email: Optional[str] = None
    password: Optional[str] = None
    username: Optional[str] = None
    is_active: Optional[bool] = None

    class Config:
        orm_mode = True




class UserSchema(BaseModel):
    id: int
    email: Optional[str] = None
    hashed_password: str
    is_active: bool


class ItemBase(BaseModel):
    title: str
    description: Optional[str] = None


class ItemCreate(ItemBase):
    pass

# me chasing a bloody mosquitos family
class Item(ItemBase):
    id: int
    owner_id: int

    class Config:
        orm_mode = True


class AuthUser(BaseModel):
    email: str
    password: str


class UserBase(BaseModel):
    email: str


class UserCreate(UserBase):
    password: str


class User(UserBase):
    id: int
    is_active: bool

    class Config:
        orm_mode = True
