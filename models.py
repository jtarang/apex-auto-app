# models.py - Models and Synchronous CRUD

from sqlalchemy import Column, Integer, String, Boolean, create_engine, select
from sqlalchemy.orm import declarative_base, Session
from pydantic import BaseModel, Field, ConfigDict
from typing import Optional, List, Any, Sequence

Base = declarative_base()


class Vehicle(Base):
    """SQLAlchemy ORM Model for the 'vehicles' table."""
    __tablename__ = "vehicles"

    id = Column(Integer, primary_key=True, index=True)
    make = Column(String, index=True, nullable=False)
    model = Column(String, index=True, nullable=False)
    year = Column(Integer, nullable=False)
    color = Column(String)
    is_available = Column(Boolean, default=True)


class VehicleBase(BaseModel):
    """Shared properties for creating and reading a vehicle."""

    make: str = Field(min_length=1)
    model: str = Field(min_length=1)
    year: int = Field(ge=1900, le=2100)
    color: Optional[str] = None
    is_available: bool = True

    model_config = ConfigDict(from_attributes=True)


class VehicleCreate(VehicleBase):
    """Properties to receive via API on creation."""
    pass


class VehicleUpdate(BaseModel):
    """Properties to receive via API on update (all fields optional)."""

    make: Optional[str] = Field(default=None, min_length=1)
    model: Optional[str] = Field(default=None, min_length=1)
    year: Optional[int] = Field(default=None, ge=1900, le=2100)
    color: Optional[str] = None
    is_available: Optional[bool] = None

    model_config = ConfigDict(from_attributes=True)


class VehicleInDB(VehicleBase):
    """Properties to return to the client (includes the ID)."""
    id: int


class CRUDVehicle:
    """
    Synchronous CRUD methods for Vehicle records.
    Uses blocking SQLAlchemy Session methods.
    """

    def get_all(self, db: Session, skip: int = 0, limit: int = 100) -> Sequence[Vehicle]:
        """Read all vehicles."""
        stmt = select(Vehicle).offset(skip).limit(limit)
        return db.scalars(stmt).all()

    def get_by_id(self, db: Session, vehicle_id: int) -> Optional[Vehicle]:
        """Read a single vehicle by its ID."""
        return db.get(Vehicle, vehicle_id)

    def create(self, db: Session, vehicle_in: VehicleCreate) -> Vehicle:
        """Create a new vehicle record."""
        vehicle_data = vehicle_in.model_dump()
        db_vehicle = Vehicle(**vehicle_data)

        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle

    def update(self, db: Session, vehicle_id: int, vehicle_in: VehicleUpdate) -> Optional[Vehicle]:
        """Update an existing vehicle record."""
        db_vehicle = self.get_by_id(db, vehicle_id)
        if not db_vehicle:
            return None

        update_data = vehicle_in.model_dump(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_vehicle, key, value)

        db.add(db_vehicle)
        db.commit()
        db.refresh(db_vehicle)
        return db_vehicle

    def delete(self, db: Session, vehicle_id: int) -> bool:
        """Delete a vehicle record."""
        db_vehicle = self.get_by_id(db, vehicle_id)
        if db_vehicle:
            db.delete(db_vehicle)
            db.commit()
            return True
        return False