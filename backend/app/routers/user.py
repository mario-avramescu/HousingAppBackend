from fastapi import APIRouter, status

from app.dependencies import HousingServiceDep, UserDep
from app.schemas.user import UserProfileResponse

router = APIRouter(prefix="/user", tags=["user"])


@router.get("/me", response_model=UserProfileResponse, status_code=status.HTTP_200_OK)
def read_user(user: UserDep, housing_service: HousingServiceDep):
    listed_housing = housing_service.get_all_listed_housing_by_owner_id(user.id)
    bought_housing = housing_service.get_all_bought_housing_by_owner_id(user.id)

    return {**user.model_dump(), "listed_housing": listed_housing, "bought_housing": bought_housing}
