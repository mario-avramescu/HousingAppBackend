from pydantic import BaseModel, ConfigDict, Field

from app.schemas.housing import HousingProfileResponse


class UserBase(BaseModel):
    username: str = Field(min_length=5, max_length=25)


class UserCreate(UserBase):
    password: str = Field(min_length=8, max_length=32)


class UserResponse(UserBase):
    id: int


class UserProfileResponse(UserBase):
    id: int
    listed_housing: list[HousingProfileResponse]
    bought_housing: list[HousingProfileResponse]

    model_config = ConfigDict(from_attributes=True)
