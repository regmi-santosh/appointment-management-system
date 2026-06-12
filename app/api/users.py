from fastapi import APIRouter, Depends, HTTPException, status

from ..schemas.user import UserCreate, User as UserSchema
from ..services.user_service import UserService, get_user_service

router = APIRouter()


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(u: UserCreate, svc: UserService = Depends(get_user_service)):
    try:
        created = svc.create_user(email=u.email, full_name=u.full_name)
    except ValueError as e:
        raise HTTPException(status_code=400, detail=str(e))
    return UserSchema(id=created.id, email=created.email, full_name=created.full_name)


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, svc: UserService = Depends(get_user_service)):
    user = svc.get_user(user_id)
    if not user:
        raise HTTPException(status_code=404, detail="user not found")
    return UserSchema(id=user.id, email=user.email, full_name=user.full_name)
