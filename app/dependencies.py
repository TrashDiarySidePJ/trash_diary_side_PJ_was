from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from app.core.security import decode_token
from app.database import get_db

bearer_scheme = HTTPBearer()

def get_current_user(
  credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
  conn = Depends(get_db)
): -> :
  payload = decode_token(credentials.credentials)
  if not payload or payload.get("type") != "access":
    raise HTTPException(
        status_code=status.HTTP_401_UNAUTHORIZED,
        detail="유효하지 않은 토큰입니다."
    )