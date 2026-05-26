from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from app.models.register import RegisterUse

class Vehicle(SQLModel, table=True):
    __tablename__ = "vehicles"
    id: Optional[int] = Field(default=None, primary_key=True)
    model: str
    year: int
    placas: str
    vin: str

    registers: list["RegisterUse"] = Relationship(back_populates="vehicle")