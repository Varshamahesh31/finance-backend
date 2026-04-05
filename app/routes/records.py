from fastapi import APIRouter, Depends, HTTPException, Query, Request
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date
from .. import schemas, dependencies
from ..services import record_service
from ..limiter import limiter

router = APIRouter(
    prefix="/records",
    tags=["records"]
)

@router.post(
    "/", 
    response_model=schemas.APIResponse[schemas.Record], 
    status_code=201, 
    summary="Create a new financial record", 
    description="Admin only. Creates a new income or expense record in the system.",
    responses={
        400: {"description": "Invalid Input Data"},
        403: {"description": "Access Denied (Not an Admin)"}
    }
)
@limiter.limit("60/minute")
def create_record(request: Request, record: schemas.RecordCreate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    new_record = record_service.create_record(db=db, record=record)
    return {"status": "success", "message": "Record created successfully", "data": new_record}

@router.get(
    "/", 
    response_model=schemas.PaginatedResponse[schemas.Record], 
    summary="Retrieve financial records", 
    description="Retrieve financial records with optional filters for search keyword, type, category, start_date, and end_date. Supports pagination via page and limit.",
    responses={
        400: {"description": "Invalid Query Parameters"},
        403: {"description": "Access Denied"}
    }
)
@limiter.limit("60/minute")
def read_records(
    request: Request,
    search: Optional[str] = Query(None, description="Search by category or notes keyword"),
    type: Optional[str] = Query(None, description="Filter by income or expense"),
    category: Optional[str] = Query(None, description="Filter by category"),
    start_date: Optional[date] = Query(None, description="Filter from start date YYYY-MM-DD"),
    end_date: Optional[date] = Query(None, description="Filter to end date YYYY-MM-DD"),
    page: int = Query(1, ge=1, description="Page number for pagination"),
    limit: int = Query(10, ge=1, le=100, description="Number of items per page"),
    db: Session = Depends(dependencies.get_db),
    current_user = Depends(dependencies.require_viewer_or_higher)
):
    total, records = record_service.get_records(
        db, 
        record_type=type, 
        category=category, 
        start_date=start_date, 
        end_date=end_date,
        search=search,
        page=page,
        limit=limit
    )
    return {
        "page": page,
        "limit": limit,
        "total": total,
        "records": records
    }

@router.get(
    "/{record_id}", 
    response_model=schemas.APIResponse[schemas.Record], 
    summary="Get a record by ID", 
    description="Fetches a single financial record based on its unique ID.",
    responses={
        403: {"description": "Access Denied"},
        404: {"description": "Record not found"}
    }
)
@limiter.limit("60/minute")
def read_record(request: Request, record_id: int, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_viewer_or_higher)):
    db_record = record_service.get_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "success", "message": "Record fetched successfully", "data": db_record}

@router.put(
    "/{record_id}", 
    response_model=schemas.APIResponse[schemas.Record], 
    summary="Update a record by ID", 
    description="Admin only. Upates details for an existing financial record.",
    responses={
        400: {"description": "Invalid Body Parameters"},
        403: {"description": "Access Denied"},
        404: {"description": "Record not found"}
    }
)
@limiter.limit("60/minute")
def update_record(request: Request, record_id: int, record: schemas.RecordUpdate, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    db_record = record_service.update_record(db, record_id=record_id, record=record)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "success", "message": "Record updated successfully", "data": db_record}

@router.delete(
    "/{record_id}", 
    response_model=schemas.APIResponse[schemas.Record], 
    summary="Delete a record by ID", 
    description="Admin only. Deletes a financial record from the database entirely.",
    responses={
        403: {"description": "Access Denied"},
        404: {"description": "Record not found"}
    }
)
@limiter.limit("60/minute")
def delete_record(request: Request, record_id: int, db: Session = Depends(dependencies.get_db), current_user = Depends(dependencies.require_admin)):
    db_record = record_service.delete_record(db, record_id=record_id)
    if db_record is None:
        raise HTTPException(status_code=404, detail="Record not found")
    return {"status": "success", "message": "Record deleted successfully", "data": db_record}
