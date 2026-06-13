from typing import Optional, List

from fastapi import Depends

from app.appointments.repository import AppointmentRepository, AppointmentRecord
from app.appointments.sqlite_repository import get_repo
from app.users.errors import RepositoryError
from datetime import datetime
from app.users.repository import get_repo as get_user_repo


class AppointmentService:
    def __init__(self, repo: AppointmentRepository):
        self._repo = repo

    def create_appointment(self, title: str, description: Optional[str], start_time, end_time, owner_id: int) -> AppointmentRecord:
        # start_time/end_time are datetime objects (validated by Pydantic)
        s, e = start_time, end_time
        if s >= e:
            raise ValueError("start_time must be before end_time")
        # validate owner exists
        user = get_user_repo().get(owner_id)
        if user is None:
            raise ValueError("owner_id does not reference an existing user")
        try:
            # store as ISO strings
            s_text = s.isoformat()
            e_text = e.isoformat()
            return self._repo.create(title=title, description=description, start_time=s_text, end_time=e_text, owner_id=owner_id)
        except Exception:
            raise RepositoryError("failed to create appointment")

    def get_appointment(self, appointment_id: int) -> Optional[AppointmentRecord]:
        return self._repo.get(appointment_id)

    def list_appointments_for_owner(self, owner_id: int) -> List[AppointmentRecord]:
        return self._repo.list_by_owner(owner_id)

    def update_appointment(self, appointment_id: int, **fields) -> AppointmentRecord:
        # validate time fields if present (Pydantic gives datetimes)
        if "start_time" in fields or "end_time" in fields:
            cur = self._repo.get(appointment_id)
            if cur is None:
                raise ValueError("appointment not found")
            # cur fields are stored as strings; parse to datetime
            old_start = self._parse_iso(cur.start_time)
            old_end = self._parse_iso(cur.end_time)
            start = fields.get("start_time", old_start)
            end = fields.get("end_time", old_end)
            if isinstance(start, str):
                start = self._parse_iso(start)
            if isinstance(end, str):
                end = self._parse_iso(end)
            if start >= end:
                raise ValueError("start_time must be before end_time")
        # convert any datetime fields to ISO strings for storage
        store_fields = {}
        for k, v in fields.items():
            if k in ("start_time", "end_time") and v is not None:
                store_fields[k] = v.isoformat() if hasattr(v, "isoformat") else v
            else:
                store_fields[k] = v
        updated = self._repo.update(appointment_id, **store_fields)
        if updated is None:
            raise ValueError("appointment not found")
        return updated

    def delete_appointment(self, appointment_id: int) -> None:
        ok = self._repo.delete(appointment_id)
        if not ok:
            raise ValueError("appointment not found")

    def _parse_iso(self, s: str) -> datetime:
        # accept trailing Z as UTC
        if s.endswith("Z"):
            s = s[:-1] + "+00:00"
        return datetime.fromisoformat(s)


def get_appointment_service() -> AppointmentService:
    return AppointmentService(get_repo())


def get_appointment_service_dep(repo: AppointmentRepository = Depends(get_repo)) -> AppointmentService:
    """FastAPI dependency that provides an AppointmentService bound to a repo.

    Use this in route `Depends()` so tests can override `app.dependency_overrides[get_repo]`.
    """
    return AppointmentService(repo)
