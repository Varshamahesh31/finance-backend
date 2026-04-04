from sqlalchemy.orm import Session
from sqlalchemy import extract
from .. import models, schemas
from typing import Optional

def get_records(
    db: Session, 
    record_type: Optional[str] = None, 
    category: Optional[str] = None, 
    start_date: Optional[str] = None,
    end_date: Optional[str] = None,
    skip: int = 0,
    limit: int = 10
):
    query = db.query(models.Record)
    
    if record_type:
        query = query.filter(models.Record.type == record_type)
    if category:
        query = query.filter(models.Record.category == category)
    if start_date:
        query = query.filter(models.Record.date >= start_date)
    if end_date:
        query = query.filter(models.Record.date <= end_date)
        
    return query.offset(skip).limit(limit).all()

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
