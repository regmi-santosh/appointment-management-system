import os
import time
from typing import Optional

import jwt


def _secret() -> str:
    s = os.environ.get("APP_SECRET")
    if not s:
        s = "dev-secret"
    return s


def create_access_token(user_id: int, expires_in: int = 3600) -> str:
    payload = {"uid": user_id, "exp": int(time.time()) + expires_in}
    token = jwt.encode(payload, _secret(), algorithm="HS256")
    if isinstance(token, bytes):
        return token.decode("utf-8")
    return token


def verify_token(token: str) -> Optional[int]:
    try:
        payload = jwt.decode(token, _secret(), algorithms=["HS256"])
        return int(payload.get("uid"))
    except Exception:
        return None
