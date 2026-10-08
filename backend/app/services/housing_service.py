from collections.abc import Sequence

import pandas as pd
from sklearn.pipeline import Pipeline
from sqlalchemy import Row, select, update
from sqlalchemy.exc import SQLAlchemyError
from sqlalchemy.orm import Session

from app.models.housing import Housing
from app.models.user import User
from app.schemas.housing import HousingBase, HousingCreate, HousingUpdate


class HousingService:
    def __init__(self, db: Session):
        self.db = db

    def get_listed_housing_by_id(self, housing_id: int) -> Row | None:
        stmt = (
            select(Housing, User.username)
            .join(User, Housing.owner_id == User.id)
            .where(Housing.id == housing_id, Housing.is_sold.is_(False))
        )

        return self.db.execute(stmt).first()

    def get_all_listed_housing(self) -> Sequence[Row]:
        stmt = (
            select(Housing, User.username)
            .join(User, Housing.owner_id == User.id)
            .where(Housing.is_sold.is_(False))
        )

        return self.db.execute(stmt).all()

    def get_all_listed_housing_by_owner_id(self, owner_id: int) -> Sequence[Housing]:
        stmt = select(Housing).where(Housing.owner_id == owner_id, Housing.is_sold.is_(False))
        return self.db.scalars(stmt).all()

    def get_all_bought_housing_by_owner_id(self, owner_id: int) -> Sequence[Housing]:
        stmt = select(Housing).where(Housing.owner_id == owner_id, Housing.is_sold.is_(True))
        return self.db.scalars(stmt).all()

    def _get_owner_id_by_housing_id(self, housing_id: int) -> int | None:
        stmt = select(Housing.owner_id).where(Housing.id == housing_id)
        return self.db.scalar(stmt)

    def get_owner_username_by_housing_id(self, housing_id: int) -> str | None:
        owner_id = self._get_owner_id_by_housing_id(housing_id)
        if owner_id is None:
            return None

        stmt = select(User.username).where(User.id == owner_id)
        return self.db.scalar(stmt)

    def create_housing(self, housing_req: HousingCreate, owner_id: int) -> Housing | None:
        housing_model = Housing(**housing_req.model_dump(), owner_id=owner_id)

        try:
            self.db.add(housing_model)
            self.db.commit()
            self.db.refresh(housing_model)
            return housing_model

        except SQLAlchemyError:
            self.db.rollback()
            return None

    def update_housing(
        self, updated_housing_req: HousingUpdate, housing_id: int, owner_id: int
    ) -> bool:
        updated_housing = updated_housing_req.model_dump(exclude_unset=True)

        stmt = (
            update(Housing)
            .where(
                Housing.id == housing_id,
                Housing.owner_id == owner_id,
                Housing.is_sold.is_(False),
            )
            .values(**updated_housing)
        )

        try:
            result = self.db.execute(stmt)

            if result.rowcount == 0:
                return False

            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            return False

    def buy_housing(self, housing_id: int, buyer_id: int) -> None:
        stmt = (
            update(Housing)
            .where(
                Housing.id == housing_id,
                Housing.is_sold.is_(False),
                Housing.owner_id != buyer_id,
            )
            .values(is_sold=True, owner_id=buyer_id)
        )

        try:
            result = self.db.execute(stmt)

            if result.rowcount == 0:
                return False

            self.db.commit()
            return True
        except SQLAlchemyError:
            self.db.rollback()
            return False


def suggest_housing_price(model: Pipeline, housing_req: HousingBase):
    df = pd.DataFrame([housing_req.model_dump()])
    prediction = model.predict(df)
    return int(prediction[0])
