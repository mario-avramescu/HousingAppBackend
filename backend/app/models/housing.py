from sqlalchemy import Boolean, Column, Float, ForeignKey, Integer, String

from app.db.database import Base


class Housing(Base):
    __tablename__ = "housing"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    longitude = Column(Float)
    latitude = Column(Float)
    housing_median_age = Column(Integer)
    total_rooms = Column(Integer)
    total_bedrooms = Column(Integer)
    population = Column(Integer)
    households = Column(Integer)
    median_income = Column(Float)
    ocean_proximity = Column(String)
    median_house_value = Column(Integer)
    owner_id = Column(Integer, ForeignKey("users.id"))
    is_sold = Column(Boolean, default=False)
