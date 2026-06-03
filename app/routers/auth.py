from fastapi import APIRouter, Depends, HTTPException, status
from psycopg2.extensions import connection
from app.database import get_db
from app.core.security import (
    hash_password,
    verify_password,
    create_access_token,
    create_refresh_token,
    decode_token
)
from app.redis_client import save_refresh_token, get_refresh_token_owner, delete_refresh_token
from app.schemas.auth import RegisterRequest, LoginRequest, RefreshRequest, TokenResponse
from app.schemas.user import UserResponse
import psycopg2.extras
from datetime import datetime

router = APIRouter(prefix="/auth", tags=["Auth"])


@router.post("/register", response_model=UserResponse, status_code=201)
def register(body: RegisterRequest, conn: connection = Depends(get_db)):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT user_id FROM users WHERE email = %s", (body.email,))
        if cur.fetchone():
            raise HTTPException(status_code=400, detail="이미 등록된 이메일입니다.")
        cur.execute(
            "INSERT INTO users(email, password, nickname, created_at) VALUES (%s, %s, %s, %s) RETURNING user_id, email, nickname, created_at",
            (body.email, hash_password(body.password), body.nickname, datetime.now())
        )
        user = cur.fetchone()
    return user


@router.post("/login", response_model=TokenResponse)
def login(body: LoginRequest, conn: connection = Depends(get_db)):
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute("SELECT user_id, password FROM users WHERE email = %s", (body.email,))
        user = cur.fetchone()

    if not user or not verify_password(body.password, user["password"]):
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="이메일 또는 비밀번호가 올바르지 않습니다.")

    access_token = create_access_token(user["user_id"])
    refresh_token, jti = create_refresh_token(user["user_id"])
    save_refresh_token(jti, user["user_id"])

    return TokenResponse(access_token=access_token, refresh_token=refresh_token)


@router.post("/refresh", response_model=TokenResponse)
def refresh(body: RefreshRequest):
    payload = decode_token(body.refresh_token)
    if not payload or payload.get("type") != "refresh":
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="유효하지 않은 리프레시 토큰입니다.")

    jti = payload.get("jti")
    owner = get_refresh_token_owner(jti)
    if not owner:
        raise HTTPException(status_code=status.HTTP_401_UNAUTHORIZED, detail="만료되거나 취소된 리프레시 토큰입니다.")

    user_id = int(owner)
    delete_refresh_token(jti)

    new_access = create_access_token(user_id)
    new_refresh, new_jti = create_refresh_token(user_id)
    save_refresh_token(new_jti, user_id)

    return TokenResponse(access_token=new_access, refresh_token=new_refresh)


@router.post("/logout", status_code=204)
def logout(body: RefreshRequest):
    payload = decode_token(body.refresh_token)
    if payload and payload.get("type") == "refresh" and payload.get("jti"):
        delete_refresh_token(payload["jti"])