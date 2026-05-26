from sqlmodel import SQLModel, Field, Relationship
from typing import Optional
from datetime import datetime

from app.models.user import User
from app.models.vehicle import Vehicle

class RegisterUse(SQLModel, table=True):
    __tablename__ = "registers"
    id: Optional[int] = Field(default=None, primary_key=True)
    user_id: int = Field(foreign_key="users.id")
    vehicle_id: int = Field(foreign_key="vehicles.id")
    date_out: datetime = Field(default_factory=datetime.utcnow)
    date_in: Optional[datetime] = None
    km_start: Optional[int] = None
    km_end: Optional[int] = None
    motive: Optional[str] = None
    gas_level: Optional[str] = None
    observations_start: Optional[str] = None
    observations_end: Optional[str] = None

    user: Optional["User"] = Relationship(back_populates="registers")
    vehicle: Optional["Vehicle"] = Relationship(back_populates="registers")
