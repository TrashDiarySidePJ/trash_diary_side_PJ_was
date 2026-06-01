from psycopg2.pool import SimpleConnectionPool
from app.core.config import DATABASE_URL

pool =  SimpleConnectionPool(1, 10, DATABASE_URL)