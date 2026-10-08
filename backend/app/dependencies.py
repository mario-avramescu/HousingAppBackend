from typing import Annotated

import jwt
from fastapi import Depends, HTTPException, Request, status
from fastapi.security import OAuth2PasswordBearer, OAuth2PasswordRequestForm
from jwt import InvalidTokenError
from sklearn.pipeline import Pipeline
from sqlalchemy.orm import Session

from app.core.config import ALGORITHM, SECRET_KEY
from app.db.database import SessionLocal
from app.schemas.user import UserResponse
from app.services.auth_service import AuthService
from app.services.housing_service import HousingService

oauth2_bearer = OAuth2PasswordBearer(tokenUrl="/auth/token")


def _get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()


DBSessionDep = Annotated[Session, Depends(_get_db)]
TokenDep = Annotated[str, Depends(oauth2_bearer)]
AuthFormDep = Annotated[OAuth2PasswordRequestForm, Depends()]


def _get_current_user(token: TokenDep) -> UserResponse:
    try:
        payload = jwt.decode(token, SECRET_KEY, algorithms=ALGORITHM)
    except InvalidTokenError:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Invalid user!",
            headers={"WWW-Authenticate": "Bearer"},
        ) from None

    username: str | None = payload.get("sub")
    user_id: int | None = payload.get("id")

    if username is None or user_id is None:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="This user doesn't exist!"
        )

    return UserResponse(username=username, id=user_id)


UserDep = Annotated[UserResponse, Depends(_get_current_user)]


def _get_auth_service(db: DBSessionDep) -> AuthService:
    return AuthService(db)


AuthServiceDep = Annotated[AuthService, Depends(_get_auth_service)]


def _get_housing_service(db: DBSessionDep) -> HousingService:
    return HousingService(db)


HousingServiceDep = Annotated[HousingService, Depends(_get_housing_service)]


def _get_model(request: Request) -> Pipeline:
    return request.app.state.model


ModelDep = Annotated[Pipeline, Depends(_get_model)]
