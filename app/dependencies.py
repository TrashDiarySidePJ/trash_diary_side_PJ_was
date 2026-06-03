from fastapi import Depends, HTTPException, status
from fastapi.security import HTTPBearer, HTTPAuthorizationCredentials
from psycopg2.extensions import connection
from app.core.security import decode_token
from app.database import get_db
import psycopg2.extras

bearer_scheme = HTTPBearer()

def get_current_user(
    credentials: HTTPAuthorizationCredentials = Depends(bearer_scheme),
    conn: connection = Depends(get_db)
) -> dict:
    # 1. 헤더에서 토큰 꺼내서 검증
    payload = decode_token(credentials.credentials)
    if not payload or payload.get("type") != "access":
        raise HTTPException(
            status_code=status.HTTP_401_UNAUTHORIZED,
            detail="유효하지 않은 토큰입니다."
        )

    # 2. DB에서 유저 조회
    with conn.cursor(cursor_factory=psycopg2.extras.RealDictCursor) as cur:
        cur.execute(
            "SELECT user_id, email, nickname FROM users WHERE user_id = %s",
            (int(payload["sub"]),)
        )
        user = cur.fetchone()

    # 3. 유저 없으면 에러
    if not user:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail="유저를 찾을 수 없습니다."
        )

    return user