from pydantic import BaseModel, EmailStr, Field
from typing import Optional, List
from datetime import date
from .models import RoleEnum, StatusEnum, TypeEnum

class UserBase(BaseModel):
    name: str
    email: EmailStr
    role: RoleEnum = RoleEnum.viewer
    status: StatusEnum = StatusEnum.active

class UserCreate(UserBase):
    pass

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be strictly positive")
    type: TypeEnum
    category: str
    date: date
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    user_id: int

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TypeEnum] = None
    category: Optional[str] = None
    date: Optional[date] = None
    notes: Optional[str] = None

class Record(RecordBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True

class SummaryCategory(BaseModel):
    category: str
    total: float

class SummaryMonthly(BaseModel):
    month: str
    income: float
    expense: float
