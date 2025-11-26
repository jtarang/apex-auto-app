from fastapi import FastAPI, Depends, HTTPException, status
from sqlalchemy.orm import Session
from typing import List

from handlers.database import DatabaseManager
from models import Base, VehicleCreate, VehicleInDB, VehicleUpdate, CRUDVehicle

database_manager = DatabaseManager()
Base.metadata.create_all(bind=database_manager.engine)
vehicle_crud = CRUDVehicle()

app = FastAPI(
    title="Apex Auto Inventory",
    description="CRUD API for vehicle inventory.",
)

@app.post("/vehicles/", response_model=VehicleInDB, status_code=status.HTTP_201_CREATED)
def create_vehicle(vehicle_in: VehicleCreate, db: Session = Depends(database_manager.get_db_session)):
    return vehicle_crud.create(db, vehicle_in)

@app.get("/vehicles/", response_model=List[VehicleInDB])
def read_vehicles(skip: int = 0, limit: int = 100, db: Session = Depends(database_manager.get_db_session)):
    return vehicle_crud.get_all(db, skip=skip, limit=limit)

@app.get("/vehicles/{vehicle_id}", response_model=VehicleInDB)
def read_vehicle(vehicle_id: int, db: Session = Depends(database_manager.get_db_session)):
    db_vehicle = vehicle_crud.get_by_id(db, vehicle_id)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@app.patch("/vehicles/{vehicle_id}", response_model=VehicleInDB)
def update_vehicle_endpoint(vehicle_id: int, vehicle_in: VehicleUpdate, db: Session = Depends(database_manager.get_db_session)):
    db_vehicle = vehicle_crud.update(db, vehicle_id, vehicle_in)
    if db_vehicle is None:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return db_vehicle

@app.delete("/vehicles/{vehicle_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_vehicle_endpoint(vehicle_id: int, db: Session = Depends(database_manager.get_db_session)):
    success = vehicle_crud.delete(db, vehicle_id)
    if not success:
        raise HTTPException(status_code=404, detail="Vehicle not found")
    return {}