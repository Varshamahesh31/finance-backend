from fastapi import APIRouter, Depends, HTTPException, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from .. import schemas, dependencies
from ..services import record_service

router = APIRouter(
    prefix="/records",
    tags=["records"]
)

@router.post(
    "/", 
    response_model=schemas.Record, 
    status_code=201, 
    summary="Create a new financial record", 
    description="Admin only. Creates a new income or expense record in the system.",
    responses={
        400: {"description": "Invalid Input Data"},
        403: {"description": "Access Denied (Not an Admin)"}
    }
)
def create_record(record: schemas.RecordCreate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    return record_service.create_record(db=db, record=record)

@router.get(
    "/", 
    response_model=List[schemas.Record], 
    summary="Retrieve financial records", 
    description="Retrieve financial records with optional filters for type, category, start_date, and end_date. Supports pagination via skip and limit.",
    responses={
        400: {"description": "Invalid Query Parameters"},
        403: {"description": "Access Denied"}
    }
)
def read_records(
    type: Optional[str] = Query(None, description="Filter by income or expense"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[str] = Query(None, description="Filter from start date YYYY-MM-DD"),
    end_date: Optional[str] = Query(None, description="Filter to end date YYYY-MM-DD"),
    skip: int = Query(0, ge=0, description="Number of items to skip"),
    limit: int = Query(10, ge=1, le=100, description="Number of items to return"),
    db: Session = Depends(dependencies.get_db),
    current_user = Depends(dependencies.require_viewer_or_higher)
):
    records = record_service.get_records(
        db, 
        record_type=type, 
        category=category, 
        start_date=start_date, 
        end_date=end_date,
        skip=skip,
        limit=limit
    )
    return records

@router.get(
    "/{record_id}", 
    response_model=schemas.Record, 
    summary="Get a record by ID", 
    description="Fetches a single financial record based on its unique ID.",
    responses={
        403: {"description": "Access Denied"},
        404: {"description": "Record not found"}
    }
)
def read_record(record_id: int, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_viewer_or_higher)):
    db_record = record_service.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.put(
    "/{record_id}", 
    response_model=schemas.Record, 
    summary="Update a record by ID", 
    description="Admin only. Upates details for an existing financial record.",
    responses={
        400: {"description": "Invalid Body Parameters"},
        403: {"description": "Access Denied"},
        404: {"description": "Record not found"}
    }
)
def update_record(record_id: int, record: schemas.RecordUpdate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    db_record = record_service.update_record(db, record_id=record_id, record=record)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record

@router.delete(
    "/{record_id}", 
    response_model=schemas.Record, 
    summary="Delete a record by ID", 
    description="Admin only. Deletes a financial record from the database entirely.",
    responses={
        403: {"description": "Access Denied"},
        404: {"description": "Record not found"}
    }
)
def delete_record(record_id: int, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    db_record = record_service.delete_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return db_record
