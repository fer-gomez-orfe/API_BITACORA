from sqlmodel import SQLModel, Field
from typing import Optional

class Usuario(SQLModel, table=True):
    id: Optional[int] = Field(default=None, primary_key=True)
    fullname: str
    username: str = Field(index=True, unique=True)
    password_hash: str