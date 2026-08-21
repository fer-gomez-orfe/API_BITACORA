from sqlmodel import SQLModel

class VehicleCreate(SQLModel):
    model: str
    placas: str
    year: int
    vin: str

class VehicleResponse(SQLModel):
    id: int
    model: str
    placas: str
    year: int
    vin: str

class VehicleResponseWithStatus(VehicleResponse):
    status: str

