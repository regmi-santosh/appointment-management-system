from pydantic import BaseModel, EmailStr, Field


class UserCreate(BaseModel):
    email: EmailStr
    full_name: str = Field(..., min_length=1)


class User(UserCreate):
    id: int
