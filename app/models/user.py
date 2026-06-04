from sqlalchemy import Column, BigInteger, String, DateTime, ForeignKey
from datetime import datetime

from app.models.base import Base

class User(Base):
    __tablename__ = "users"

    user_id = Column(BigInteger, primary_key=True)
    email = Column(String(100), nullable=False, unique=True)
    password = Column(String(255), nullable=False)
    name = Column(String(20), nullable=False)
    nickname = Column(String(30), nullable=False)
    phone = Column(String(30), nullable=False, unique=True)
    created_at = Column(DateTime, nullable=False, default=datetime.now)
    mode_id = Column(BigInteger, ForeignKey("modes.mode_id"), nullable=False, default=1)