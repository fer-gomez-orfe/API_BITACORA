from pwdlib import PasswordHash
import jwt
from datetime import datetime, timedelta
from app.core.config import SECRET_KEY



ALGORITHM = "HS256"

pwd_context = PasswordHash.recommended()

# Generar hash
def hash_password(password: str):
    return pwd_context.hash(password)

# Verificar password
def verify_password(
    plain_password: str,
    hashed_password: str
):
    return pwd_context.verify(
        plain_password,
        hashed_password
    )

# Crear token JWT
def create_access_token(data: dict):
    to_encode = data.copy()

    expire = datetime.utcnow() + timedelta(hours=10)

    to_encode.update({"exp": expire})

    return jwt.encode(
        to_encode,
        SECRET_KEY,
        algorithm=ALGORITHM
    )