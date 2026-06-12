from typing import Dict
from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel, EmailStr, Field

router = APIRouter()


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1)


class User(UserCreate):
    id: int


# simple in-memory store (id -> User)
_store: Dict[int, User] = {}
_next_id = 1


@router.post("/", response_model=User, status_code=status.HTTP_201_CREATED)
def create_user(u: UserCreate):
    global _next_id
    # simple uniqueness check by email
    for existing in _store.values():
        if existing.email == u.email:
            raise HTTPException(status_code=400, detail="email already exists")

    user = User(id=_next_id, **u.dict())
    _store[_next_id] = user
    _next_id += 1
    return user


@router.get("/{user_id}", response_model=User)
def get_user(user_id: int):
    user = _store.get(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return user
