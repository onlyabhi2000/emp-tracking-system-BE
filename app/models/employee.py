from sqlalchemy import Column, Integer, String, Enum
from sqlalchemy.orm import relationship
from app.core.db import Base
import enum

class ShiftType(enum.Enum):
    morning = "morning"
    evening = "evening"
    night = "night"

class Employee(Base):
    __tablename__ = "employees"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, nullable=False)
    department = Column(String, nullable=True)
    current_shift = Column(Enum(ShiftType), nullable=False)

    attendances = relationship("Attendance", back_populates="employee")
