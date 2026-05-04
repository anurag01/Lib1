from fastapi import APIRouter, HTTPException, Depends, status
from pydantic import BaseModel, EmailStr
from typing import Optional, List
from sqlalchemy.orm import Session
from sqlalchemy.exc import IntegrityError
from sqlalchemy import inspect as sa_inspect
import hashlib

from app.models.base import get_db
from app.models.user import User

router = APIRouter()


class UserCreate(BaseModel):
    username: str
    email: EmailStr
    password: str


class UserUpdate(BaseModel):
    username: Optional[str] = None
    email: Optional[EmailStr] = None
    password: Optional[str] = None


class UserLogin(BaseModel):
    email: EmailStr
    password: str


class UserProfile(BaseModel):
    id: int
    username: str
    email: EmailStr


def _hash_password(raw_password: str) -> str:
    return hashlib.sha256(raw_password.encode("utf-8")).hexdigest()


def _model_columns(model_cls) -> set[str]:
    return {c.key for c in sa_inspect(model_cls).columns}


def _pick_existing_field(model_cls, candidates: list[str]) -> Optional[str]:
    cols = _model_columns(model_cls)
    for name in candidates:
        if name in cols:
            return name
    return None


ID_FIELDS = ["id", "user_id"]
USERNAME_FIELDS = ["username", "user_name", "name", "full_name"]
EMAIL_FIELDS = ["email", "email_address", "mail"]
PASSWORD_FIELDS = ["hashed_password", "password_hash", "password"]


def _set_field(obj, candidates: list[str], value):
    field = _pick_existing_field(type(obj), candidates)
    if not field:
        raise HTTPException(status_code=500, detail=f"User model missing fields: {candidates}")
    setattr(obj, field, value)


def _get_field(obj, candidates: list[str]):
    field = _pick_existing_field(type(obj), candidates)
    if not field:
        raise HTTPException(status_code=500, detail=f"User model missing fields: {candidates}")
    return getattr(obj, field)


def _to_profile(user_obj: User) -> UserProfile:
    return UserProfile(
        id=_get_field(user_obj, ID_FIELDS),
        username=_get_field(user_obj, USERNAME_FIELDS),
        email=_get_field(user_obj, EMAIL_FIELDS),
    )


@router.post("/users/", response_model=UserProfile, status_code=status.HTTP_201_CREATED)
def create_user(user: UserCreate, db: Session = Depends(get_db)):
    new_user = User()
    _set_field(new_user, USERNAME_FIELDS, user.username)
    _set_field(new_user, EMAIL_FIELDS, str(user.email))
    _set_field(new_user, PASSWORD_FIELDS, _hash_password(user.password))

    try:
        db.add(new_user)
        db.commit()
        db.refresh(new_user)
        return _to_profile(new_user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")


@router.post("/users/login", response_model=UserProfile)
def login_user(payload: UserLogin, db: Session = Depends(get_db)):
    email_field = _pick_existing_field(User, EMAIL_FIELDS)
    if not email_field:
        raise HTTPException(status_code=500, detail="User model missing email field")

    user = db.query(User).filter(getattr(User, email_field) == str(payload.email)).first()
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    stored_hash = _get_field(user, PASSWORD_FIELDS)
    if stored_hash != _hash_password(payload.password):
        raise HTTPException(status_code=401, detail="Invalid password")

    return _to_profile(user)


@router.get("/users/{user_id}", response_model=UserProfile)
def get_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")
    return _to_profile(user)


@router.put("/users/{user_id}", response_model=UserProfile)
def update_user(user_id: int, payload: UserUpdate, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    if payload.username is not None:
        _set_field(user, USERNAME_FIELDS, payload.username)
    if payload.email is not None:
        _set_field(user, EMAIL_FIELDS, str(payload.email))
    if payload.password is not None:
        _set_field(user, PASSWORD_FIELDS, _hash_password(payload.password))

    try:
        db.commit()
        db.refresh(user)
        return _to_profile(user)
    except IntegrityError:
        db.rollback()
        raise HTTPException(status_code=400, detail="Username or email already exists")


@router.delete("/users/{user_id}", status_code=status.HTTP_200_OK)
def delete_user(user_id: int, db: Session = Depends(get_db)):
    user = db.get(User, user_id)
    if not user:
        raise HTTPException(status_code=404, detail="User not found")

    db.delete(user)
    db.commit()
    return {"detail": "User deleted successfully"}


@router.get("/users/", response_model=List[UserProfile])
def get_all_users(db: Session = Depends(get_db)):
    users = db.query(User).all()
    return [_to_profile(u) for u in users]
