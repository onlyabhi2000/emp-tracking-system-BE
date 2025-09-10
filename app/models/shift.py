from sqlalchemy import Column, Integer, Enum, ForeignKey
from app.core.db import Base
from app.models.employee import ShiftType
from sqlalchemy.orm import relationship

class Shift(Base):
    __tablename__ = "shifts"

    id = Column(Integer, primary_key=True, index=True)
    week = Column(Integer, nullable=False)
    shift_type = Column(Enum(ShiftType), nullable=False)

    employee_id = Column(Integer, ForeignKey("employees.id"))
    employee = relationship("Employee", back_populates="shifts")
