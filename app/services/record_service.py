from sqlalchemy.orm import Session
from sqlalchemy import extract, or_
from .. import models, schemas
from typing import Optional, Tuple, List
from datetime import date

def get_records(
    db: Session, 
    record_type: Optional[str] = None, 
    category: Optional[str] = None, 
    start_date: Optional[date] = None,
    end_date: Optional[date] = None,
    search: Optional[str] = None,
    page: int = 1,
    limit: int = 10
) -> Tuple[int, List[models.Record]]:
    query = db.query(models.Record)
    
    if search:
        search_filter = f"%{search}%"
        query = query.filter(
            or_(
                models.Record.category.ilike(search_filter),
                models.Record.notes.ilike(search_filter)
            )
        )
        
    if record_type:
        query = query.filter(models.Record.type == record_type)
    if category:
        query = query.filter(models.Record.category == category)
    if start_date:
        query = query.filter(models.Record.date >= start_date)
    if end_date:
        query = query.filter(models.Record.date <= end_date)
        
    total = query.count()
    skip = (page - 1) * limit
    records = query.offset(skip).limit(limit).all()
    return total, records

def create_record(db: Session, record: schemas.RecordCreate):
    db_record = models.Record(**record.dict())
    db.add(db_record)
    db.commit()
    db.refresh(db_record)
    return db_record

def get_record(db: Session, record_id: int):
    return db.query(models.Record).filter(models.Record.id == record_id).first()

def update_record(db: Session, record_id: int, record: schemas.RecordUpdate):
    db_record = get_record(db, record_id)
    if db_record:
        update_data = record.dict(exclude_unset=True)
        for key, value in update_data.items():
            setattr(db_record, key, value)
        db.commit()
        db.refresh(db_record)
    return db_record

def delete_record(db: Session, record_id: int):
    db_record = get_record(db, record_id)
    if db_record:
        db.delete(db_record)
        db.commit()
    return db_record
