from datetime import timedelta

from fastapi import APIRouter, HTTPException, status
from pydantic import BaseModel

from app.core.config import ACCESS_TOKEN_EXPIRE_MINUTES
from app.core.security import create_access_token
from app.dependencies import AuthFormDep, AuthServiceDep
from app.schemas.user import UserCreate

router = APIRouter(prefix="/auth", tags=["auth"])


class Token(BaseModel):
    access_token: str
    token_type: str


@router.post("/", response_model=Token, status_code=status.HTTP_201_CREATED)
async def create_user(auth_service: AuthServiceDep, user_req: UserCreate):

    user = auth_service.create_user(user_req)
    if user is None:
        raise HTTPException(
            status_code=status.HTTP_409_CONFLICT, detail="This username already exists!"
        )

    token = create_access_token(
        user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=token, token_type="bearer")


@router.post("/token", response_model=Token, status_code=status.HTTP_201_CREATED)
async def login_for_access_token(auth_service: AuthServiceDep, form_data: AuthFormDep):
    user = auth_service.authenticate_user(form_data.username, form_data.password)

    if not user:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Could not validate user.",
            headers={"WWW-Authenticate": "Bearer"},
        )

    token = create_access_token(
        user.username, user.id, timedelta(minutes=ACCESS_TOKEN_EXPIRE_MINUTES)
    )

    return Token(access_token=token, token_type="bearer")
