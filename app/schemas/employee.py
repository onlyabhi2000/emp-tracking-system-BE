from pydantic import BaseModel
from typing import Optional, List
from app.schemas.attendance import Attendance
from app.schemas.shift import Shift
from enum import Enum

class ShiftType(str, Enum):
    morning = "morning"
    evening = "evening"
    night = "night"

class EmployeeBase(BaseModel):
    name: str
    department: Optional[str] = None
    current_shift: ShiftType

class EmployeeCreate(EmployeeBase):
    pass

class EmployeeUpdate(BaseModel):
    name: Optional[str] = None
    department: Optional[str] = None
    current_shift: Optional[ShiftType] = None

class Employee(EmployeeBase):
    id: int
    
    class Config:
        orm_mode = True

# Response Schemas with Relationships (Forward References)
class EmployeeWithAttendance(Employee):
    attendances: List['Attendance'] = []

class EmployeeWithShifts(Employee):
    shifts: List['Shift'] = []

class EmployeeComplete(Employee):
    attendances: List['Attendance'] = []
    shifts: List['Shift'] = []