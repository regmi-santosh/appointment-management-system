from typing import Optional

from app.users.domain.repository import UserRecord, UserRepository, get_repo
from app.users.domain.errors import UserAlreadyExists, UserNotFound


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def create_user(self, email: str, full_name: str) -> UserRecord:
        try:
            return self._repo.create(email=email, full_name=full_name)
        except UserAlreadyExists:
            raise
        except Exception as e:
            # wrap unexpected repository errors
            raise

    def get_user(self, user_id: int) -> Optional[UserRecord]:
        user = self._repo.get(user_id)
        if user is None:
            from app.users.domain.errors import UserNotFound

            raise UserNotFound(f"user {user_id} not found")
        return user


def get_user_service() -> UserService:
    return UserService(get_repo())
