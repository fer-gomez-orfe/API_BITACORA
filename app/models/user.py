from sqlmodel import SQLModel, Field, Relationship
from typing import Optional, List

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    fullname: str
    username: str = Field(index=True, unique=True)
    password_hash: str
    #Relacion con registros de uso de vehiculos que ha realizado el usuario 
    registers: List["RegisterUse"] = Relationship(back_populates="user")