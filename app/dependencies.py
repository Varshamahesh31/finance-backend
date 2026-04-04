from fastapi import Depends, HTTPException, Header
from sqlalchemy.orm import Session
from .database import SessionLocal
from .models import User, RoleEnum

def get_db():
    db = SessionLocal()
    try:
        yield db
    finally:
        db.close()

def get_current_user(x_user_id: int = Header(..., description="Mock authentication: send user ID in header to authenticate"), db: Session = Depends(get_db)):
    user = db.query(User).filter(User.id == x_user_id).first()
    if not user:
        raise HTTPException(status_code=401, detail="Invalid user ID in X-User-Id header")
    if user.status.value != "active":
        raise HTTPException(status_code=403, detail="Inactive user")
    return user

def require_admin(current_user: User = Depends(get_current_user)):
    if current_user.role != RoleEnum.admin:
        raise HTTPException(status_code=403, detail="Admin access required")
    return current_user

def require_analyst_or_admin(current_user: User = Depends(get_current_user)):
    if current_user.role not in [RoleEnum.analyst, RoleEnum.admin]:
        raise HTTPException(status_code=403, detail="Analyst or Admin access required")
    return current_user

# Viewers can view records and summaries, so basically anyone authenticated can view them.
def require_viewer_or_higher(current_user: User = Depends(get_current_user)):
    return current_user
