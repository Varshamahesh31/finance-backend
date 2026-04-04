from sqlalchemy.orm import Session
from sqlalchemy import func, extract
from .. import models

def get_total_income(db: Session):
    result = db.query(func.sum(models.Record.amount)).filter(models.Record.type == models.TypeEnum.income).scalar()
    return result or 0.0

def get_total_expense(db: Session):
    result = db.query(func.sum(models.Record.amount)).filter(models.Record.type == models.TypeEnum.expense).scalar()
    return result or 0.0

def get_net_balance(db: Session):
    return get_total_income(db) - get_total_expense(db)

def get_category_totals(db: Session):
    results = db.query(models.Record.category, func.sum(models.Record.amount)).group_by(models.Record.category).all()
    return [{"category": row[0], "total": row[1]} for row in results]

def get_recent_transactions(db: Session, limit: int = 10):
    return db.query(models.Record).order_by(models.Record.date.desc()).limit(limit).all()

def get_monthly_trends(db: Session):
    # This queries income/expense grouped by year-month
    # SQLite logic
    results = db.query(
        func.strftime("%Y-%m", models.Record.date).label("month"),
        models.Record.type,
        func.sum(models.Record.amount)
    ).group_by("month", models.Record.type).all()
    
    monthly_data = {}
    for row in results:
        month, t_type, amount = row[0], row[1], row[2]
        if month not in monthly_data:
            monthly_data[month] = {"month": month, "income": 0.0, "expense": 0.0}
        
        if t_type == models.TypeEnum.income:
            monthly_data[month]["income"] += amount
        else:
            monthly_data[month]["expense"] += amount
            
    # sort by month desc
    return sorted(list(monthly_data.values()), key=lambda x: x["month"], reverse=True)
