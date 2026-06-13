import sqlite3
from dataclasses import dataclass
from typing import Optional, List
import abc

from app.core.db import get_connection
from app.users.errors import RepositoryError


@dataclass
class AppointmentRecord:
    id: int
    title: str
    description: Optional[str]
    start_time: str
    end_time: str
    owner_id: int


class AppointmentRepository(abc.ABC):
    @abc.abstractmethod
    def create(self, title: str, description: Optional[str], start_time: str, end_time: str, owner_id: int) -> AppointmentRecord:
        ...

    @abc.abstractmethod
    def get(self, appointment_id: int) -> Optional[AppointmentRecord]:
        ...

    @abc.abstractmethod
    def list_by_owner(self, owner_id: int) -> List[AppointmentRecord]:
        ...

    def update(self, appointment_id: int, **fields) -> Optional[AppointmentRecord]:
        """Optional update operation; concrete repos should implement if supported."""
        raise NotImplementedError

    def delete(self, appointment_id: int) -> bool:
        """Optional delete operation; concrete repos should implement if supported."""
        raise NotImplementedError
