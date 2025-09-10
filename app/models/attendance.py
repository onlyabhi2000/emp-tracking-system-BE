from sqlalchemy import Column, Integer, DateTime, ForeignKey, String
from sqlalchemy.orm import relationship
from app.core.db import Base
import datetime

class Attendance(Base):
    __tablename__ = "attendance"

    id = Column(Integer, primary_key=True, index=True)
    employee_id = Column(Integer, ForeignKey("employees.id"), nullable=False)
    login_time = Column(DateTime, default=datetime.datetime.utcnow)
    logout_time = Column(DateTime, nullable=True)

    employee = relationship("Employee", back_populates="attendances")
