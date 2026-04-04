from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, dependencies
from ..services import record_service

router = APIRouter(
    prefix="/records",
    tags=["records"]
)

@router.post("/", response_model=schemas.Record, status_code=201)
def create_record(record: schemas.RecordCreate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    return record_service.create_record(db=db, record=record)

@router.get("/", response_model=List[schemas.Record])
def read_records(
    type: Optional[str] = Query(None, description="Filter by income or expense"),
    category: Optional[str] = Query(None, description="Filter by category"),
    date: Optional[str] = Query(None, description="Filter by date YYYY-MM"),
    db: Session = Depends(dependencies.get_db),
    current_user = Depends(dependencies.require_viewer_or_higher)
):
    records = record_service.get_records(db, record_type=type, category=category, date_str=date)
    return records

@router.get("/{record_id}", response_model=schemas.Record)
def read_record(record_id: int, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_viewer_or_higher)):
    db_record = record_service.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.put("/{record_id}", response_model=schemas.Record)
def update_record(record_id: int, record: schemas.RecordUpdate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    db_record = record_service.update_record(db, record_id=record_id, record=record)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.delete("/{record_id}", response_model=schemas.Record)
def delete_record(record_id: int, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    db_record = record_service.delete_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record
