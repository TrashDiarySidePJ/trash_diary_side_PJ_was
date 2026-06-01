from passlib.context import CryptContext
from datetime import datetime, timedelta, timezone
from jose import jwt, JWTError
from app.core.config import SECRET_KEY, ALGORITHM, ACCESS_TOKEN_EXPIRE_MINUTES, REFRESH_TOKEN_EXPIRE_DAYS
import uuid
from typing import Optional

pwd_context = CryptContext(schemes=["bcrypt"], deprecated="auto")

def hash_password(password: str) -> str:
  return pwd_context.hash(password)
    

def verify_password(plain: str, hashed: str) -> bool:
  return pwd_context.verify(plain, hashed)

def create_access_token(user_id: int) -> str:
  expire = datetime.now(timezone.utc) + timedelta(minutes= ACCESS_TOKEN_EXPIRE_MINUTES)
  
  payload = {
    "sub": str(user_id),
    "type": "access",
    "exp": expire
  }
  
  return jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)

def create_refresh_token(user_id: int) -> tuple[str, str]:
  # jti 라는 고유 ID (Redis에서 토큰 식별용)
  jti = str(uuid.uuid4())
  expire = datetime.now(timezone.utc) + timedelta(days=REFRESH_TOKEN_EXPIRE_DAYS)
  payload = {
    "sub": str(user_id),
    "type": "refresh",
    "exp": expire,
    "jti": jti
  }
  token = jwt.encode(payload, SECRET_KEY, algorithm= ALGORITHM)
  return token , jti

def decode_token(token: str) -> Optional[dict]:
  try:
    return jwt.decode(token, SECRET_KEY, algorithms= [ALGORITHM])
  except JWTError:
    return None