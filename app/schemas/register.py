from sqlmodel import SQLModel

class UserInfo(SQLModel):
    id: int
    fullname: str

class VehicleInfo(SQLModel):
    id: int
    name: str
    placas: str

class RegisterResponse(SQLModel):
    id: int
    user: UserInfo
    vehicle: VehicleInfo
    date_out: str
    date_in: str
    km_start: int
    km_end: int
    motive: str
    gas_level: str
    observations_start: str
    observations_end: str

class RegisterOut(SQLModel):
    vehicle_id: int
    km_start: int
    motive: str
    gas_level: str
    observations_start: str

class RegisterIn(SQLModel):
    km_end: int
    gas_level: str
    observations_end: str