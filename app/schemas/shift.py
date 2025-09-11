from pydantic import BaseModel
from typing import Optional
from app.schemas.employee import ShiftType 

class ShiftBase(BaseModel):
    week: int
    shift_type: ShiftType
    employee_id: int

class ShiftCreate(ShiftBase):
    pass

class ShiftUpdate(BaseModel):
    week: Optional[int] = None
    shift_type: Optional[ShiftType] = None

class Shift(ShiftBase):
    id: int
    
    class Config:
        orm_mode = True