from fastapi import APIRouter, Depends, Request
from sqlalchemy.orm import Session
from typing import List
from .. import schemas, dependencies
from ..services import summary_service
from ..limiter import limiter

router = APIRouter(
    prefix="/summary",
    tags=["summary"],
    dependencies=[Depends(dependencies.require_viewer_or_higher)]
)

@router.get("/income", response_model=schemas.APIResponse[float], summary="Get Total Income", description="Returns the sum of all income records.")
@limiter.limit("60/minute")
def get_income(request: Request, db: Session = Depends(dependencies.get_db)):
    data = summary_service.get_total_income(db)
    return {"status": "success", "message": "Total income fetched", "data": data}

@router.get("/expense", response_model=schemas.APIResponse[float], summary="Get Total Expense", description="Returns the sum of all expense records.")
@limiter.limit("60/minute")
def get_expense(request: Request, db: Session = Depends(dependencies.get_db)):
    data = summary_service.get_total_expense(db)
    return {"status": "success", "message": "Total expense fetched", "data": data}

@router.get("/balance", response_model=schemas.APIResponse[float], summary="Get Net Balance", description="Returns the net balance (income minus expenses).")
@limiter.limit("60/minute")
def get_balance(request: Request, db: Session = Depends(dependencies.get_db)):
    data = summary_service.get_net_balance(db)
    return {"status": "success", "message": "Net balance fetched", "data": data}

@router.get("/category", response_model=schemas.APIResponse[List[schemas.SummaryCategory]], summary="Get Categories Total", description="Returns a list containing all categories and their aggregated totals.")
@limiter.limit("60/minute")
def get_categories(request: Request, db: Session = Depends(dependencies.get_db)):
    data = summary_service.get_category_totals(db)
    return {"status": "success", "message": "Category totals fetched", "data": data}

@router.get("/recent", response_model=schemas.APIResponse[List[schemas.Record]], summary="Get Recent Transactions", description="Fetches the 10 most recent records by date.")
@limiter.limit("60/minute")
def get_recent(request: Request, db: Session = Depends(dependencies.get_db)):
    data = summary_service.get_recent_transactions(db)
    return {"status": "success", "message": "Recent transactions fetched", "data": data}

@router.get("/monthly", response_model=schemas.APIResponse[List[schemas.SummaryMonthly]], summary="Get Monthly Data", description="Calculates income and expense separated by month.")
@limiter.limit("60/minute")
def get_monthly(request: Request, db: Session = Depends(dependencies.get_db)):
    data = summary_service.get_monthly_trends(db)
    return {"status": "success", "message": "Monthly statistics fetched", "data": data}
