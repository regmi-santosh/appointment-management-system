from fastapi import APIRouter, Depends, HTTPException, status

from app.users.schemas import UserCreate, User as UserSchema, LoginRequest, TokenResponse
from app.users.services import UserService, get_user_service
from app.auth import create_access_token
from app.users.domain.errors import UserAlreadyExists, UserNotFound

router = APIRouter()


@router.post("/", response_model=UserSchema, status_code=status.HTTP_201_CREATED)
def create_user(u: UserCreate, svc: UserService = Depends(get_user_service)):
    try:
        # support optional password on create
        created = svc.create_user_with_password(email=u.email, full_name=u.full_name, password=u.password)
    except UserAlreadyExists as e:
        raise HTTPException(status_code=status.HTTP_409_CONFLICT, detail=str(e))
    except ValueError as e:
        # business validation error
        raise HTTPException(status_code=status.HTTP_400_BAD_REQUEST, detail=str(e))
    return UserSchema(id=created.id, email=created.email, full_name=created.full_name)



@router.post("/login", response_model=TokenResponse)
def login(req: LoginRequest, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.authenticate_user(email=req.email, password=req.password)
    except UserNotFound:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid credentials")
    token = create_access_token(user_id=user.id)
    return TokenResponse(access_token=token)


@router.get("/{user_id}", response_model=UserSchema)
def get_user(user_id: int, svc: UserService = Depends(get_user_service)):
    try:
        user = svc.get_user(user_id)
    except UserNotFound as e:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail=str(e))
    return UserSchema(id=user.id, email=user.email, full_name=user.full_name)
