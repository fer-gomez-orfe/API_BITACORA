from fastapi import FastAPI
from app.db.database import create_db_and_tables
from app.api.routes.auth import router as auth_router
from app.api.routes.vehicles import router as vehicle_router 
from app.api.routes.records import router as records_router

app = FastAPI(
    title="API de Bitácora de Vehículos",
    description="Una API para gestionar el uso de vehículos en una empresa",
    version="1.0.0"
)

@app.on_event("startup")
def on_startup():
    create_db_and_tables()

#Router para autenticacion y gestion de usuarios
app.include_router(auth_router)

#Router para vehiculos, gestion y consultas
app.include_router(vehicle_router)

#Router para registro de uso de los vehiculos y consulta de registros
app.include_router(records_router)

@app.get("/")
def root():
    return {"message": "API funcionando con SQLModel"}

