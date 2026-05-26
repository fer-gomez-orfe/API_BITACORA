from fastapi.security import OAuth2PasswordBearer
from jose import JWTError
import jwt
from sqlmodel import Session, select
from fastapi import Depends, HTTPException, status
from app.core.security import ALGORITHM, SECRET_KEY
from app.db.database import get_session
from app.models.user import User


oauth2_scheme = OAuth2PasswordBearer(tokenUrl="login")

def get_current_user(token: str = Depends(oauth2_scheme), session: Session = Depends(get_session)):

    credentials_exception = HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="Could not validate credentials",
        headers={"WWW-Authenticate": "Bearer"},
    )

    try: 
        payload = jwt.decode(token, SECRET_KEY, algorithms=[ALGORITHM])
        print(payload)
        user_id: str = payload.get("user_id")

        if user_id is None:
            raise credentials_exception
    
    except JWTError:
        raise credentials_exception
    
    user = session.exec(select(User).where(User.id == user_id)).first()

    if not user:
        raise credentials_exception
    
    return user