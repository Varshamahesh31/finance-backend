from fastapi import APIRouter, Depends, HTTPException
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, dependencies
from ..services import user_service

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.User, status_code=201, summary="Create User", description="Admin only. Creates a new user with the specified role.")
def create_user(user: schemas.UserCreate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    """Only admins can create users."""
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    return user_service.create_user(db=db, user=user)

@router.get("/", response_model=List[schemas.User], summary="Get All Users", description="Admin only. Views all users inside the system.")
def read_users(skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    """Only admins can view users list."""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return users
