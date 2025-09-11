from pydantic import BaseModel
from typing import Optional
import datetime

class AttendanceBase(BaseModel):
    employee_id: int
    login_time: Optional[datetime.datetime] = None
    logout_time: Optional[datetime.datetime] = None

class AttendanceCreate(BaseModel):
    employee_id: int

class AttendanceLogin(BaseModel):
    employee_id: int
    login_time: datetime.datetime

class AttendanceLogout(BaseModel):
    logout_time: datetime.datetime

class AttendanceUpdate(BaseModel):
    login_time: Optional[datetime.datetime] = None
    logout_time: Optional[datetime.datetime] = None

class Attendance(AttendanceBase):
    id: int
    
    class Config:
        orm_mode = True