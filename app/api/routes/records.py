from fastapi import APIRouter, Depends, HTTPException, status
from sqlmodel import Session, select
from app.db.database import get_session
from app.models.user import User
from app.models.register import RegisterUse
from app.schemas.register import RegisterIn, RegisterOut, RegisterResponse
from app.api.deps import get_current_user
from datetime import datetime
from sqlalchemy.orm import selectinload

router = APIRouter(
    prefix="/records",
    tags=["Records"]
)

#Registrar uso de un vehiculo
@router.post("/register/out")
def register_out(
    data: RegisterOut,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    
    #Primero se verifica que el vehiculo no este en uso
    active_vehicle = session.exec(
        select(RegisterUse).where(
            RegisterUse.vehicle_id == data.vehicle_id,
            RegisterUse.date_in == None
        )   
    ).first()

    if active_vehicle:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="El vehículo ya está en uso"
        )

    register = RegisterUse(
        user_id=current_user.id,
        vehicle_id=data.vehicle_id,
        km_start=data.km_start,
        motive=data.motive,
        gas_level=data.gas_level,
        observations_start=data.observations_start
    )

    session.add(register)
    session.commit()
    session.refresh(register)

    return register

##Registrar regreso de un vehiculo
@router.post("/register/return/{register_id}")
def register_return(
    register_id: int,
    data: RegisterIn,
    session: Session = Depends(get_session),
    current_user: User = Depends(get_current_user)
):
    register = session.exec(
        select(RegisterUse).where(
            RegisterUse.id == register_id
        )
    ).first()

    if not register:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="Registro no encontrado"
        )
    
    #Opcion para validar kilometraje
    if data.km_end < register.km_start:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST,
            detail="Kilometraje final invalido"
        )
    
    register.km_end = data.km_end
    register.gas_level = data.gas_level
    register.observations_end = data.observations_end
    register.date_in = datetime.utcnow()

    session.add(register)
    session.commit()
    session.refresh(register)
    
    return register

#Consultar registro activos
@router.get("/active/records", response_model=list[RegisterResponse])
def get_active_records(session: Session = Depends(get_session), current_user: User = Depends(get_current_user)):

    records = session.exec(
        select(RegisterUse)
        .options(
            selectinload(RegisterUse.user),
            selectinload(RegisterUse.vehicle)
        )
        .where(
            RegisterUse.date_in == None
        )
    ).all()

    return records

#Consultar historial de registros
@router.get("/my/records")
def get_history(
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    register = session.exec(
        select(RegisterUse).where(RegisterUse.user_id == current_user.id)
    ).all()

    return register
