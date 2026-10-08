from sqlalchemy import select
from sqlalchemy.orm import Session

from app.core.security import check_password, hash_password
from app.models.user import User
from app.schemas.user import UserCreate


class AuthService:
    def __init__(self, db: Session):
        self.db = db

    def _get_user_by_username(self, username: str) -> User | None:
        stmt = select(User).where(User.username == username)
        return self.db.scalar(stmt)

    def create_user(self, user_req: UserCreate) -> User | None:
        if self._get_user_by_username(user_req.username):
            return None

        user_model = User(
            username=user_req.username, hashed_password=hash_password(user_req.password)
        )

        self.db.add(user_model)
        self.db.commit()
        self.db.refresh(user_model)

        return user_model

    def authenticate_user(self, username: str, password: str) -> User | None:
        user_model = self._get_user_by_username(username)
        if user_model is None:
            return None

        password_ok = check_password(password, user_model.hashed_password)
        if not password_ok:
            return None

        return user_model
