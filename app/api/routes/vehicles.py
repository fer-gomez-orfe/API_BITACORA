from fastapi import APIRouter, Depends
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.register import RegisterUse
from app.models.vehicle import Vehicle
from app.schemas.vehicle import VehicleCreate, VehicleResponse

router =  APIRouter(
    prefix="/vehicles",
    tags = ["Vehicles"]
)

@router.post("/", response_model=VehicleResponse)
def create_vehicle(data: VehicleCreate, session: Session = Depends(get_session)):

    vehicle = Vehicle(
        model = data.model,
        placas = data.placas,
        year = data.year,
        vin = data.vin
    )

    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)

    return vehicle

@router.get("/", response_model=list[VehicleResponse])
def get_vehicles(session: Session = Depends(get_session)):

    vehicles = session.exec(
        select(Vehicle)
    ).all()

    return vehicles

@router.get("/available")
def available_vehicles(session: Session = Depends(get_session)):
    actives = session.exec(
        select(RegisterUse).where(
            RegisterUse.date_in == None
        )
    ).all()

    occupied_vehicle_ids = {active.vehicle_id for active in actives}

    vehicles = session.exec(
        select(Vehicle).where(
            Vehicle.id.notin_(occupied_vehicle_ids)
        )
    ).all()

    return vehicles