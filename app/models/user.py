from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import DeclarativeBase
from datetime import datetime

class Base(DeclarativeBase):
    pass

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    nickname = Column(String(30), nullable=False)
    created_at = Column(DateTime, nullable=False, default=datetime.now)