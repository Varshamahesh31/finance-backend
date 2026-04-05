from fastapi import APIRouter, Depends, HTTPException, Request
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, dependencies
from ..services import user_service
from ..limiter import limiter

router = APIRouter(
    prefix="/users",
    tags=["users"]
)

@router.post("/", response_model=schemas.APIResponse[schemas.User], status_code=201, summary="Create User", description="Admin only. Creates a new user with the specified role.")
@limiter.limit("60/minute")
def create_user(request: Request, user: schemas.UserCreate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    """Only admins can create users."""
    db_user = user_service.get_user_by_email(db, email=user.email)
    if db_user:
        raise HTTPException(status_code=400, detail="Email already registered")
    
    new_user = user_service.create_user(db=db, user=user)
    return {"status": "success", "message": "User created successfully", "data": new_user}

@router.get("/", response_model=schemas.APIResponse[List[schemas.User]], summary="Get All Users", description="Admin only. Views all users inside the system.")
@limiter.limit("60/minute")
def read_users(request: Request, skip: int = 0, limit: int = 100, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    """Only admins can view users list."""
    users = user_service.get_users(db, skip=skip, limit=limit)
    return {"status": "success", "message": "Users retrieved successfully", "data": users}
