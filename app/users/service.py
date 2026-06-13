from typing import Optional

from passlib.context import CryptContext

from app.users.errors import UserAlreadyExists, UserNotFound
from app.users.repository import UserRecord, UserRepository, get_repo

pwd_context = CryptContext(schemes=["pbkdf2_sha256"], deprecated="auto")


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def create_user(self, email: str, full_name: str) -> UserRecord:
        try:
            return self._repo.create(email=email, full_name=full_name)
        except UserAlreadyExists:
            raise
        except Exception as e:
            raise

    def create_user_with_password(self, email: str, full_name: str, password: Optional[str] = None) -> UserRecord:
        hashed = None
        if password is not None:
            hashed = pwd_context.hash(password)
        try:
            return self._repo.create(email=email, full_name=full_name, password=hashed)
        except UserAlreadyExists:
            raise
        except Exception:
            raise

    def authenticate_user(self, email: str, password: str) -> UserRecord:
        user = self._repo.get_by_email(email)
        if user is None:
            raise UserNotFound(f"user with email {email} not found")
        if user.password is None:
            raise UserNotFound("invalid credentials")
        if not pwd_context.verify(password, user.password):
            raise UserNotFound("invalid credentials")
        return user

    def get_user(self, user_id: int) -> Optional[UserRecord]:
        user = self._repo.get(user_id)
        if user is None:
            from app.users.errors import UserNotFound

            raise UserNotFound(f"user {user_id} not found")
        return user


def get_user_service() -> UserService:
    return UserService(get_repo())
