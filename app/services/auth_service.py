from fastapi import HTTPException, status
from sqlalchemy.orm import Session
from datetime import datetime

from app.models.user import User
from app.core.security import create_access_token, create_refresh_token, decode_token, hash_password, verify_password
from app.redis_client import delete_refresh_token, get_refresh_token_owner, save_refresh_token
from app.schemas.auth import LoginRequest, RefreshRequest, RegisterRequest, TokenResponse

def register_user(body: RegisterRequest, db: Session):
    existing_email = db.query(User).filter(User.email == body.email).first()
    if existing_email:
        raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
    
    existing_phone = db.query(User).filter(User.phone == body.phone).first()

    if existing_phone:
        raise HTTPException(status_code=400, detail="이미 등록된 전화번호 입니다.")

    user = User(
        email=body.email,
        password=hash_password(body.password),
        name=body.name,
        nickname=body.nickname,
        phone=body.phone,
        mode_id=body.mode_id,
        created_at=datetime.now()
    )
    db.add(user)
    db.commit()
    db.refresh(user)
    return user

def login_user(body: LoginRequest, db: Session):
    user = db.query(User).filter(User.email == body.email).first()

    if not user or not verify_password(body.password, user.password):
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="이메일 또는 비밀번호가 올바르지 않습니다."
        )

    access_token = create_access_token(user.user_id)
    refresh_token, jti = create_refresh_token(user.user_id)
    save_refresh_token(jti, user.user_id)

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)

def refresh_token(body: RefreshRequest):
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 리프레시 토큰입니다."
        )

    jti = payload.get("jti")
    owner = get_refresh_token_owner(jti)
    if not owner:
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="만료되거나 취소된 리프레시 토큰입니다."
        )
    
    user_id = int(owner)
    delete_refresh_token(jti)
    
    new_access = create_access_token(user_id)
    new_refresh, new_jti = create_refresh_token(user_id)
    save_refresh_token(new_jti, user_id)

    return TokenResponse(access_token=new_access, refresh_token=new_refresh)
    
def logout_user(body: RefreshRequest):
    payload = decode_token(body.refresh_token)
    if payload and payload.get("type") == "refresh" and payload.get("jti"):
        delete_refresh_token(payload["jti"])