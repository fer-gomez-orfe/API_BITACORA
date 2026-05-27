from datetime import datetime
from typing import Optional

from sqlmodel import SQLModel

class UserInfo(SQLModel):
    id: int
    fullname: str

class VehicleInfo(SQLModel):
    id: int
    model: str
    placas: str

class RegisterResponse(SQLModel):
    id: int
    user: UserInfo
    vehicle: VehicleInfo
    date_out: datetime
    date_in: Optional[datetime] = None
    km_start: int
    km_end: Optional[int] = None
    motive: str
    gas_level: str
    observations_start: str
    observations_end: Optional[str] = None

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