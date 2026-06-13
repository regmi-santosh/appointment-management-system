import sqlite3
from dataclasses import dataclass
from typing import Optional, List

from app.core.db import get_connection
from app.users.errors import RepositoryError
from app.appointments.repository import AppointmentRecord, AppointmentRepository


class SQLiteAppointmentRepository(AppointmentRepository):
    def __init__(self):
        pass

    def create(self, title: str, description: Optional[str], start_time: str, end_time: str, owner_id: int) -> AppointmentRecord:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute(
                "INSERT INTO appointments (title, description, start_time, end_time, owner_id) VALUES (?, ?, ?, ?, ?)",
                (title, description, start_time, end_time, owner_id),
            )
            conn.commit()
            appt_id = cur.lastrowid
            return AppointmentRecord(id=appt_id, title=title, description=description, start_time=start_time, end_time=end_time, owner_id=owner_id)
        except Exception as e:
            raise RepositoryError(str(e))
        finally:
            conn.close()

    def get(self, appointment_id: int) -> Optional[AppointmentRecord]:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, title, description, start_time, end_time, owner_id FROM appointments WHERE id = ?", (appointment_id,))
            row = cur.fetchone()
            if not row:
                return None
            return AppointmentRecord(id=row[0], title=row[1], description=row[2], start_time=row[3], end_time=row[4], owner_id=row[5])
        finally:
            conn.close()

    def list_by_owner(self, owner_id: int) -> List[AppointmentRecord]:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("SELECT id, title, description, start_time, end_time, owner_id FROM appointments WHERE owner_id = ?", (owner_id,))
            rows = cur.fetchall()
            return [AppointmentRecord(id=r[0], title=r[1], description=r[2], start_time=r[3], end_time=r[4], owner_id=r[5]) for r in rows]
        finally:
            conn.close()

    def update(self, appointment_id: int, **fields) -> Optional[AppointmentRecord]:
        conn = get_connection()
        cur = conn.cursor()
        try:
            sets = []
            vals = []
            for k, v in fields.items():
                sets.append(f"{k} = ?")
                vals.append(v)
            if not sets:
                return self.get(appointment_id)
            vals.append(appointment_id)
            sql = f"UPDATE appointments SET {', '.join(sets)} WHERE id = ?"
            cur.execute(sql, tuple(vals))
            conn.commit()
            return self.get(appointment_id)
        finally:
            conn.close()

    def delete(self, appointment_id: int) -> bool:
        conn = get_connection()
        cur = conn.cursor()
        try:
            cur.execute("DELETE FROM appointments WHERE id = ?", (appointment_id,))
            conn.commit()
            return cur.rowcount > 0
        finally:
            conn.close()


def get_repo() -> SQLiteAppointmentRepository:
    return SQLiteAppointmentRepository()
