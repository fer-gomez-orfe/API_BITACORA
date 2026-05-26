from sqlmodel import SQLModel, Field, Relationship
from typing import Optional

from app.models.register import RegisterUse

class User(SQLModel, table=True):
    __tablename__ = "users"
    id: Optional[int] = Field(default=None, primary_key=True)
    fullname: str
    username: str = Field(index=True, unique=True)
    password_hash: str
    registers: list["RegisterUse"] = Relationship(back_populates="user")