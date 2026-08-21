from fastapi import APIRouter, Depends, HTTPException
from sqlmodel import Session, select
from app.api.deps import get_current_user
from app.db.database import get_session
from app.models.user import User
from app.schemas.user import UserResponse, UserLogin, UserCreate
from app.core.security import hash_password, verify_password, create_access_token

router = APIRouter(
    prefix="/auth",
    tags=["Auth"]
)

@router.post("/signup", response_model=UserResponse)
def register(data: UserCreate, session: Session = Depends(get_session)):
    
    existing_user = session.exec(
        select(User).where(
            User.username == data.username
        )
    ).first()

    if existing_user:
        raise HTTPException(
            status_code=400, 
            detail="El nombre de usuario ya está en uso"
            )
    
    user = User(
        fullname=data.fullname,
        username=data.username,
        password_hash=hash_password(data.password)
    )

    session.add(user)
    session.commit()
    session.refresh(user)

    return user

@router.post("/login")
def login(data: UserLogin, session: Session = Depends(get_session)):

    user = session.exec(
        select(User).where(
            User.username == data.username
            )
    ).first()

    if not user or not verify_password(data.password, user.password_hash):
        raise HTTPException(
            status_code=400,
            detail="Credenciales inválidas"
        )

    access_token = create_access_token(
        data={"user_id": user.id}
    )

    return {"access_token": access_token, "token_type": "bearer"}

@router.get("/me")
def me(current_user: User = Depends(get_current_user)):
    return UserResponse.model_validate(current_user)