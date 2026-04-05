from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional
from datetime import date

import models, schemas, crud
from database import get_db

router = APIRouter(prefix="/api", tags=["tasks"])

# ==================== TASK MANAGEMENT ====================

@router.get("/tasks", response_model=List[schemas.TaskOut])
def list_tasks(
	skip: int = Query(0, ge=0),
	limit: int = Query(100, ge=1, le=1000),
	priority: Optional[str] = None,
	category: Optional[str] = None,
	db: Session = Depends(get_db)
):
	"""List all tasks with optional filtering by priority or category"""
	return crud.get_tasks(db, skip=skip, limit=limit, priority=priority, category=category)

@router.post("/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED)
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
	"""Create a new task"""  
	return crud.create_task(db=db, task=task)

@router.get("/tasks/{task_id}", response_model=schemas.TaskOut)
def get_task(task_id: int, db: Session = Depends(get_db)):
	"""Get a specific task by ID"""
	db_task = crud.get_task(db, task_id=task_id)
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return db_task

@router.put("/tasks/{task_id}", response_model=schemas.TaskOut)
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
	"""Update a task"""
	updated = crud.update_task(db=db, task_id=task_id, task=task)
	if updated is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return updated

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_task(task_id: int, db: Session = Depends(get_db)):
	"""Delete a task"""
	deleted = crud.delete_task(db=db, task_id=task_id)
	if deleted is None:
		raise HTTPException(status_code=404, detail="Task not found")

# ==================== QUICK VIEWS ====================

@router.get("/tasks/view/today", response_model=List[schemas.TaskOut])
def get_today_tasks(db: Session = Depends(get_db)):
	"""Get all tasks due today"""
	return crud.get_today_tasks(db)

@router.get("/tasks/view/overdue", response_model=List[schemas.TaskOut])
def get_overdue_tasks(db: Session = Depends(get_db)):
	"""Get all overdue incomplete tasks"""
	return crud.get_overdue_tasks(db)

@router.get("/tasks/view/upcoming", response_model=List[schemas.TaskOut])
def get_upcoming(
	days: int = Query(7, ge=1, le=90),
	db: Session = Depends(get_db)
):
	"""Get tasks due in the next N days"""
	return crud.get_upcoming_tasks(db, days=days)

@router.get("/tasks/view/pending", response_model=List[schemas.TaskOut])
def get_pending(db: Session = Depends(get_db)):
	"""Get all incomplete tasks"""
	return crud.get_pending_tasks(db)

@router.get("/tasks/view/completed", response_model=List[schemas.TaskOut])
def get_completed(
	skip: int = Query(0, ge=0),
	limit: int = Query(50, ge=1, le=500),
	db: Session = Depends(get_db)
):
	"""Get completed tasks"""
	return crud.get_completed_tasks(db, skip=skip, limit=limit)

# ==================== CATEGORY MANAGEMENT ====================

@router.get("/categories", response_model=List[str])
def get_categories(db: Session = Depends(get_db)):
	"""Get all task categories"""
	return crud.get_categories(db)

@router.get("/tasks/category/{category}", response_model=List[schemas.TaskOut])
def get_tasks_by_category(
	category: str,
	skip: int = Query(0, ge=0),
	limit: int = Query(100, ge=1, le=1000),
	db: Session = Depends(get_db)
):
	"""Get all tasks in a specific category"""
	return crud.get_tasks_by_category(db, category=category, skip=skip, limit=limit)

# ==================== AGENDA / SCHEDULE ====================

@router.get("/agenda/date/{date_str}", response_model=List[schemas.TaskOut])
def get_agenda_date(date_str: str, db: Session = Depends(get_db)):
	"""Get all tasks for a specific date (YYYY-MM-DD)"""
	try:
		target_date = date.fromisoformat(date_str)
	except ValueError:
		raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
	return crud.get_agenda_for_date(db, target_date)

@router.get("/agenda/range", response_model=List[schemas.TaskOut])
def get_agenda_range(
	start: str = Query(..., description="Start date (YYYY-MM-DD)"),
	end: str = Query(..., description="End date (YYYY-MM-DD)"),
	db: Session = Depends(get_db)
):
	"""Get all tasks between two dates"""
	try:
		start_date = date.fromisoformat(start)
		end_date = date.fromisoformat(end)
	except ValueError:
		raise HTTPException(status_code=400, detail="Invalid date format. Use YYYY-MM-DD")
	
	if start_date > end_date:
		raise HTTPException(status_code=400, detail="Start date must be before end date")
	
	return crud.get_agenda_range(db, start_date, end_date)

# ==================== STATISTICS ====================

@router.get("/stats", response_model=schemas.TaskStatistics)
def get_statistics(db: Session = Depends(get_db)):
	"""Get task statistics and analytics"""
	return crud.get_task_statistics(db)

# ==================== HEALTH CHECK ====================

@router.get("/", tags=["system"])
def root():
	"""API root endpoint"""
	return {
		"message": "Simple TODO App API",
		"version": "1.0.0",
		"endpoints": {
			"tasks": "CRUD operations for tasks",
			"quick_views": "Today, Upcoming, Pending, Completed, Overdue",
			"agenda": "Calendar/schedule views by date range",
			"categories": "Manage task categories",
			"stats": "Task statistics and analytics"
		}
	}

@router.get("/health", tags=["system"])
def health_check():
	"""Health check endpoint"""
	return {"status": "healthy", "service": "TODO App"}
