import os
import time
from typing import Optional

import jwt
from fastapi import Header, HTTPException, status


def get_current_user_id(authorization: Optional[str] = Header(None)) -> int:
    if not authorization:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="missing authorization")
    parts = authorization.split()
    if len(parts) != 2 or parts[0].lower() != "bearer":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid auth scheme")
    token = parts[1]
    uid = verify_token(token)
    if uid is None:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="invalid token")
    return uid


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
