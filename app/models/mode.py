from sqlalchemy import Column, BigInteger, String, DateTime
from sqlalchemy.orm import relationship

from app.models.base import Base

class User(Base):
    __tablename__ = "modes"

    mode_id = Column(BigInteger, primary_key=True)
    moed_name = Column(String(30), nullable=False, unique=True)

    users = relationship("User", back_populates="mode")