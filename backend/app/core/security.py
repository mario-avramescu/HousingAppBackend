from datetime import datetime, timedelta, timezone

import bcrypt
import jwt

from app.core.config import ALGORITHM, SECRET_KEY


def hash_password(password: str) -> str:
    pwd_bytes = password.encode()
    salt = bcrypt.gensalt()
    hashed_password = bcrypt.hashpw(pwd_bytes, salt).decode()
    return hashed_password


def check_password(password: str, hashed_password: str) -> bool:
    pwd_bytes = password.encode()
    hashed_pwd_bytes = hashed_password.encode()
    return bcrypt.checkpw(pwd_bytes, hashed_pwd_bytes)


def create_access_token(username: str, user_id: int, expires_delta: timedelta):
    encode = {"sub": username, "id": user_id}
    expires = datetime.now(timezone.utc) + expires_delta
    encode.update({"exp": expires})

    return jwt.encode(encode, SECRET_KEY, algorithm=ALGORITHM)
