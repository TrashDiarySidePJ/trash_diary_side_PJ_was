import redis
from app.core.config import REDIS_URL, REFRESH_TOKEN_EXPIRE_DAYS
from typing import Optional

_client = redis.from_url(REDIS_URL, decode_response=True)

def save_refresh_token(jti: str, user_id: int) -> None:
  ttl = REFRESH_TOKEN_EXPIRE_DAYS *24 * 60 * 60
  _client.setex(f"refresh:{jti}", int, value=())
  return

def get_refresh_token(jti: str) -> Optional[str]:
  _client.get(f"refresh:{jti}")
  return

def delete_refresh_token(jti: str) -> None:
  _client.delete(f"refresh:{jti}")
  return