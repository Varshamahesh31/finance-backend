from fastapi import APIRouter, Depends
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, dependencies
from ..services import summary_service

router = APIRouter(
    prefix="/summary",
    tags=["summary"],
    dependencies=[Depends(dependencies.require_viewer_or_higher)]
)

@router.get("/income", response_model=float)
def get_income(db: Session = Depends(dependencies.get_db)):
    return summary_service.get_total_income(db)

@router.get("/expense", response_model=float)
def get_expense(db: Session = Depends(dependencies.get_db)):
    return summary_service.get_total_expense(db)

@router.get("/balance", response_model=float)
def get_balance(db: Session = Depends(dependencies.get_db)):
    return summary_service.get_net_balance(db)

@router.get("/category", response_model=List[schemas.SummaryCategory])
def get_categories(db: Session = Depends(dependencies.get_db)):
    return summary_service.get_category_totals(db)

@router.get("/recent", response_model=List[schemas.Record])
def get_recent(db: Session = Depends(dependencies.get_db)):
    return summary_service.get_recent_transactions(db)

@router.get("/monthly", response_model=List[schemas.SummaryMonthly])
def get_monthly(db: Session = Depends(dependencies.get_db)):
    return summary_service.get_monthly_trends(db)
