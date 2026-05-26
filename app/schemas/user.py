from sqlmodel import SQLModel

# Datos para registro
class UserCreate(SQLModel):
    fullname: str
    username: str
    password: str

# Datos para login
class UserLogin(SQLModel):
    username: str
    password: str

# Respuesta API
class UserResponse(SQLModel):
    id: int
    fullname: str
    username: str