from datetime import datetime

from sqlalchemy import Column, DateTime, Integer, String, Text
from sqlalchemy.sql import func

from .connection import Base


class OfficeModel(Base):
    __tablename__ = "offices"
    
    office_id = Column(Integer, primary_key=True, autoincrement=False)
    name = Column(String(100), nullable=False)
    capacity = Column(Integer, nullable=False, default=1)
    description = Column(Text, nullable=True)
    
    def __repr__(self) -> str:
        return f"<OfficeModel(id={self.office_id}, name='{self.name}')>"


class ReservationModel(Base):
    __tablename__ = "reservations"
    
    reservation_id = Column(Integer, primary_key=True, autoincrement=True)
    office_id = Column(Integer, nullable=False)
    
    user_name = Column(String(200), nullable=False)
    user_email = Column(String(200), nullable=False)
    user_phone = Column(String(50), nullable=False)
    
    start_time = Column(DateTime, nullable=False)
    end_time = Column(DateTime, nullable=False)
    
    status = Column(String(20), nullable=False, default="pending")
    created_at = Column(DateTime, nullable=False, server_default=func.now())
    
    def __repr__(self) -> str:
        return (
            f"<ReservationModel(id={self.reservation_id}, "
            f"office_id={self.office_id}, status='{self.status}')>"
        )
