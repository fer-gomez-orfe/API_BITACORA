from datetime import datetime
from fastapi import FastAPI, Depends, HTTPException, status
from sqlmodel import Session, select
from app.api.deps import get_current_user
from app.db.database import create_db_and_tables, get_session
from app.models.user import User
from app.schemas.user import UserCreate, UserLogin, UserResponse
from app.core.security import hash_password, verify_password, create_access_token
from app.models.vehicle import Vehicle
from app.models.register import RegisterUse
from app.schemas.vehicle import VehicleCreate, VehicleResponse
from app.schemas.register import RegisterIn, RegisterOut, RegisterResponse
from sqlalchemy.orm import selectinload

app = FastAPI()

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

@app.get("/")
def root():
    return {"message": "API funcionando con SQLModel"}

# Endpoint de prueba para insertar usuario
@app.post("/register", response_model=UserResponse)
def register(data: UserCreate, session: Session = Depends(get_session)):
    
    # Verificar si el username ya existe
    existing_user = session.exec(
        select(User).where(User.username == data.username)
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=status.HTTP_400_BAD_REQUEST, 
            detail="Username ya existe"
            )
    
    # Crear nuevo usuario
    user = User(
        fullname=data.fullname,
        username=data.username,
        password_hash=hash_password(data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

# Login del usuario

@app.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):
    user = session.exec(
        select(User).where(User.username == data.username)
    ).first()


    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="Credenciales inválidas"
        )
    
    # Crear token JWT con el userid como sub
    token = create_access_token({"user_id": user.id})

    return {"access_token": token, "token_type": "bearer"}


#Consultar lista de vehiculos
@app.get("/vehicles", response_model=list[VehicleResponse])
def get_vehicles(session: Session = Depends(get_session)):
    vehicles = session.exec(select(Vehicle)).all()
    return vehicles

#Dar de alta un nuevo vehiculo
@app.post("/vehicles", response_model=VehicleResponse)
def add_vehicle(data: VehicleCreate, session: Session = Depends(get_session)):

    vehicle = Vehicle(
        model = data.model,
        year=data.year,
        placas=data.placas,
        vin=data.vin
    )

    session.add(vehicle)
    session.commit()
    session.refresh(vehicle)

    return vehicle

#Registrar uso de un vehiculo
@app.post("/register/out")
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
@app.post("/register/return/{register_id}")
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
@app.get("/active/records", response_model=list[RegisterResponse])
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
@app.get("/my/records")
def get_history(
    session: Session = Depends(get_session), 
    current_user: User = Depends(get_current_user)
):
    register = session.exec(
        select(RegisterUse).where(RegisterUse.user_id == current_user.id)
    ).all()

    return register
