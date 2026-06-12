from fastapi import APIRouter, Depends, HTTPException, status

from app.users.schemas import UserCreate, User as UserSchema
from app.users.services import UserService, get_user_service
from app.users.domain.errors import UserAlreadyExists, UserNotFound

router = APIRouter()


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(u: UserCreate, svc: UserService = Depends(get_user_service)):
    try:
        created = svc.create_user(email=u.email, full_name=u.full_name)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        # business validation error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return UserSchema(id=created.id, email=created.email, full_name=created.full_name)


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.get_user(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return UserSchema(id=user.id, email=user.email, full_name=user.full_name)
