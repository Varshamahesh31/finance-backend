from sqlalchemy.orm import Session
from sqlalchemy import extract
from .. import models, schemas
from typing import Optional

def get_records(db: Session, record_type: Optional[str] = None, category: Optional[str] = None, date_str: Optional[str] = None):
    query = db.query(models.Record)
    
    if record_type:
        query = query.filter(models.Record.type == record_type)
    if category:
        query = query.filter(models.Record.category == category)
    if date_str:
        # Assuming date_str is "YYYY-MM"
        try:
            year, month = map(int, date_str.split("-"))
            query = query.filter(extract('year', models.Record.date) == year)
            query = query.filter(extract('month', models.Record.date) == month)
        except ValueError:
            pass # Invalid format, ignore or handle differently. We assume valid format here as per requirements.
            
    return query.all()

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
