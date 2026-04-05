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
    class Config:
        schema_extra = {
            "example": {
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "role": "viewer",
                "status": "active"
            }
        }

class User(UserBase):
    id: int

    class Config:
        orm_mode = True
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 1,
                "name": "Jane Doe",
                "email": "jane.doe@example.com",
                "role": "viewer",
                "status": "active"
            }
        }

class RecordBase(BaseModel):
    amount: float = Field(..., gt=0, description="Amount must be strictly positive")
    type: TypeEnum
    category: str = Field(..., min_length=1, description="Category cannot be empty")
    date: date
    notes: Optional[str] = None

class RecordCreate(RecordBase):
    user_id: int
    
    class Config:
        schema_extra = {
            "example": {
                "amount": 250.50,
                "type": "expense",
                "category": "Food",
                "date": "2026-04-10",
                "notes": "Lunch bill",
                "user_id": 1
            }
        }

class RecordUpdate(BaseModel):
    amount: Optional[float] = Field(None, gt=0)
    type: Optional[TypeEnum] = None
    category: Optional[str] = Field(None, min_length=1)
    date: Optional[date] = None
    notes: Optional[str] = None

class Record(RecordBase):
    id: int
    user_id: int

    class Config:
        orm_mode = True
        from_attributes = True
        schema_extra = {
            "example": {
                "id": 100,
                "amount": 250.50,
                "type": "expense",
                "category": "Food",
                "date": "2026-04-10",
                "notes": "Lunch bill",
                "user_id": 1
            }
        }

class SummaryCategory(BaseModel):
    category: str
    total: float

class SummaryMonthly(BaseModel):
    month: str
    income: float
    expense: float

from typing import Generic, TypeVar, Any

T = TypeVar('T')

class APIResponse(BaseModel, Generic[T]):
    status: str = "success"
    message: str = "Operation completed"
    data: T

class PaginatedResponse(BaseModel, Generic[T]):
    page: int
    limit: int
    total: int
    records: List[T]
