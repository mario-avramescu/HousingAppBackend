from fastapi import APIRouter, HTTPException, Path, status

from app.dependencies import HousingServiceDep, ModelDep, UserDep
from app.schemas.housing import (
    HousingBase,
    HousingCreate,
    HousingPublicResponse,
    HousingUpdate,
    HousingValueSuggested,
)
from app.services.housing_service import suggest_housing_price

router = APIRouter(prefix="/housing", tags=["housing"])


@router.get("/", response_model=list[HousingPublicResponse], status_code=status.HTTP_200_OK)
def read_all_listed_housing(housing_service: HousingServiceDep):
    results = housing_service.get_all_listed_housing()

    if not results:
        raise HTTPException(status_code=status.HTTP_404_NOT_FOUND, detail="No housing available!")

    response_list: list[HousingPublicResponse] = []

    for listed_housing, owner_username in results:
        response_list.append({**vars(listed_housing), "owner_username": owner_username})

    return response_list


@router.get(
    "/{housing_id}",
    response_model=HousingPublicResponse,
    status_code=status.HTTP_200_OK,
)
def read_listed_housing_by_id(housing_service: HousingServiceDep, housing_id: int = Path(ge=1)):
    result = housing_service.get_listed_housing_by_id(housing_id)

    if not result:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND, detail="Housing not found or already sold!"
        )

    listed_housing, owner_username = result

    return {**vars(listed_housing), "owner_username": owner_username}


@router.post("/sell-housing", status_code=status.HTTP_201_CREATED)
def create_housing(user: UserDep, housing_service: HousingServiceDep, housing_req: HousingCreate):
    housing = housing_service.create_housing(housing_req, user.id)
    if housing is None:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, detail="Housing could not be created!"
        )
    return {"message": "Housing successfully listed!"}


@router.put("/buy-housing/{housing_id}", status_code=status.HTTP_204_NO_CONTENT)
def buy_housing(user: UserDep, housing_service: HousingServiceDep, housing_id: int = Path(ge=1)):
    success = housing_service.buy_housing(housing_id, user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="You cannot buy this house. It might not exist, is already sold, or you already own it.",
        )


@router.put("/update-housing/{housing_id}", status_code=status.HTTP_204_NO_CONTENT)
def update_housing(
    user: UserDep,
    housing_service: HousingServiceDep,
    housing_req: HousingUpdate,
    housing_id: int = Path(ge=1),
):
    success = housing_service.update_housing(housing_req, housing_id, user.id)
    if not success:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Housing could not be updated. It might be sold or you are not the owner.",
        )


@router.post(
    "/suggested-price", response_model=HousingValueSuggested, status_code=status.HTTP_200_OK
)
def predict_price(user: UserDep, model: ModelDep, housing_req: HousingBase):
    price = suggest_housing_price(model, housing_req)
    return HousingValueSuggested(suggested_median_house_value=price)
