from enum import StrEnum

from pydantic import BaseModel, ConfigDict, Field


class OceanProximity(StrEnum):
    LESS_THAN_1H_OCEAN = "<1H OCEAN"
    INLAND = "INLAND"
    NEAR_OCEAN = "NEAR OCEAN"
    NEAR_BAY = "NEAR BAY"
    ISLAND = "ISLAND"


class HousingBase(BaseModel):
    model_config = ConfigDict(use_enum_values=True)

    longitude: float = Field(ge=-124.35, le=-114.31)
    latitude: float = Field(ge=32.54, le=41.95)
    housing_median_age: int = Field(ge=1, le=52)
    total_rooms: int = Field(ge=2, le=39320)
    total_bedrooms: int = Field(ge=1, le=6445)
    population: int = Field(ge=3, le=35682)
    households: int = Field(ge=1, le=6082)
    median_income: float = Field(
        ge=0.4999,
        le=15.0001,
        description="Median income in tens of thousands of USD (e.g. 3.5 = $35,000)",
    )
    ocean_proximity: OceanProximity


class HousingCreate(HousingBase):
    name: str = Field(min_length=5, max_length=25)
    median_house_value: int = Field(gt=0, description="Price set by the user, in USD")


class HousingUpdate(HousingCreate):
    pass


class HousingPublicResponse(HousingCreate):
    id: int
    owner_id: int
    owner_username: str | None = None
    is_sold: bool = Field(default=False)

    model_config = ConfigDict(from_attributes=True)


class HousingProfileResponse(HousingCreate):
    model_config = ConfigDict(from_attributes=True)


class HousingValueSuggested(BaseModel):
    suggested_median_house_value: int = Field(
        ge=0,
        description="Model-predicted median house value in USD",
    )
