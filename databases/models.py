from sqlalchemy import Column, Integer, String, Text, DateTime, ForeignKey
from .database import Base

class Device(Base):
    __tablename__ = "devices"
    id = Column(Integer, primary_key=True, index=True)
    name = Column(String(64), nullable=False, index=True)
    status = Column(Integer, nullable=False, index=True)