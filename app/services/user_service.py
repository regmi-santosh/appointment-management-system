from typing import Optional

from ..repository import UserRecord, UserRepository, get_repo


class UserService:
    def __init__(self, repo: UserRepository):
        self._repo = repo

    def create_user(self, email: str, full_name: str) -> UserRecord:
        try:
            return self._repo.create(email=email, full_name=full_name)
        except Exception as e:
            # simplify DB-specific exceptions into ValueError for API layer
            if 'UNIQUE' in str(e):
                raise ValueError('email already exists')
            raise

    def get_user(self, user_id: int) -> Optional[UserRecord]:
        return self._repo.get(user_id)


def get_user_service() -> UserService:
    return UserService(get_repo())
