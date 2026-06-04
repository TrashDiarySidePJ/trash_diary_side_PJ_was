from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from app.database import get_db
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, TokenResponse
from app.schemas.user import UserResponse
from app.services.auth_service import login_user, logout_user, refresh_token, register_user

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(body:RegisterRequest, db: Session = Depends(get_db)):
    return register_user(body, db)

@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, db: Session = Depends(get_db)):
    return login_user(body, db)

@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest):
    return refresh_token(body)


@router.post("/logout", status_code=204)
def logout(body: RefreshRequest):
    return logout_user(body)