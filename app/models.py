from sqlalchemy import Column, Integer, String, Float, Enum, Date, ForeignKey
from sqlalchemy.orm import relationship
import enum
from .database import Base

class RoleEnum(str, enum.Enum):
    viewer = "viewer"
    analyst = "analyst"
    admin = "admin"

class StatusEnum(str, enum.Enum):
    active = "active"
    inactive = "inactive"

class TypeEnum(str, enum.Enum):
    income = "income"
    expense = "expense"

class User(Base):
    __tablename__ = "users"

    id = Column(Integer, primary_key=True, index=True)
    name = Column(String, index=True)
    email = Column(String, unique=True, index=True)
    role = Column(Enum(RoleEnum), default=RoleEnum.viewer)
    status = Column(Enum(StatusEnum), default=StatusEnum.active)

    records = relationship("Record", back_populates="user")

class Record(Base):
    __tablename__ = "records"

    id = Column(Integer, primary_key=True, index=True)
    amount = Column(Float, nullable=False)
    type = Column(Enum(TypeEnum), nullable=False)
    category = Column(String, nullable=False, index=True)
    date = Column(Date, nullable=False, index=True)
    notes = Column(String)
    user_id = Column(Integer, ForeignKey("users.id"))

    user = relationship("User", back_populates="records")