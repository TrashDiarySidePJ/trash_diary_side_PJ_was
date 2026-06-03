from psycopg2.pool import SimpleConnectionPool
from app.core.config import DATABASE_URL

pool =  SimpleConnectionPool(1, 10, DATABASE_URL)

def get_db():
  connect = pool.getconn()
  try:
    yield connect
    connect.commit()
  except Exception:
    connect.rollback()
    raise
  finally:
    pool.putconn(connect)