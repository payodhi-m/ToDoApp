from fastapi import APIRouter, Depends, HTTPException, status, Query
from sqlalchemy.orm import Session
from typing import List, Optional

import models, schemas, crud
from database import get_db

router = APIRouter()

# ==================== TASK MANAGEMENT ====================

@router.get("/tasks", response_model=List[schemas.TaskOut], tags=["tasks"])
def list_tasks(
	skip: int = Query(0, ge=0),
	limit: int = Query(100, ge=1, le=1000),
	status: Optional[str] = None,
	priority: Optional[str] = None,
	db: Session = Depends(get_db)
):
	"""List all tasks with optional filtering"""
	return crud.get_tasks(db, skip=skip, limit=limit, status=status, priority=priority)

@router.post("/tasks", response_model=schemas.TaskOut, status_code=status.HTTP_201_CREATED, tags=["tasks"])
def create_task(task: schemas.TaskCreate, db: Session = Depends(get_db)):
	"""Create a new task"""
	return crud.create_task(db=db, task=task)

@router.get("/tasks/{task_id}", response_model=schemas.TaskDetailedOut, tags=["tasks"])
def get_task(task_id: int, db: Session = Depends(get_db)):
	"""Get a specific task"""
	db_task = crud.get_task(db, task_id=task_id)
	if db_task is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return db_task

@router.put("/tasks/{task_id}", response_model=schemas.TaskOut, tags=["tasks"])
def update_task(task_id: int, task: schemas.TaskUpdate, db: Session = Depends(get_db)):
	"""Update a task"""
	updated = crud.update_task(db=db, task_id=task_id, task=task)
	if updated is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return updated

@router.delete("/tasks/{task_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["tasks"])
def delete_task(task_id: int, db: Session = Depends(get_db)):
	"""Delete a task"""
	deleted = crud.delete_task(db=db, task_id=task_id)
	if deleted is None:
		raise HTTPException(status_code=404, detail="Task not found")

# ==================== TASK EXECUTION ====================

@router.post("/tasks/{task_id}/complete", response_model=schemas.TaskOut, tags=["execution"])
def complete_task(task_id: int, execution_time_ms: Optional[float] = None, db: Session = Depends(get_db)):
	"""Mark a task as completed"""
	result = crud.mark_task_completed(db, task_id, execution_time_ms)
	if result is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return result

@router.post("/tasks/{task_id}/fail", response_model=schemas.TaskOut, tags=["execution"])
def fail_task(task_id: int, error_message: str, db: Session = Depends(get_db)):
	"""Mark a task as failed"""
	result = crud.mark_task_failed(db, task_id, error_message)
	if result is None:
		raise HTTPException(status_code=404, detail="Task not found")
	return result

@router.get("/tasks/pending", response_model=List[schemas.TaskOut], tags=["execution"])
def get_pending_tasks(db: Session = Depends(get_db)):
	"""Get all pending tasks ready for execution"""
	return crud.get_pending_tasks(db)

@router.get("/tasks/overdue", response_model=List[schemas.TaskOut], tags=["execution"])
def get_overdue_tasks(db: Session = Depends(get_db)):
	"""Get all overdue tasks"""
	return crud.get_overdue_tasks(db)

# ==================== TASK FILTERING ====================

@router.get("/tasks/category/{category}", response_model=List[schemas.TaskOut], tags=["filtering"])
def get_tasks_by_category(category: str, db: Session = Depends(get_db)):
	"""Get all tasks in a specific category"""
	tasks = crud.get_tasks_by_category(db, category)
	if not tasks:
		raise HTTPException(status_code=404, detail="No tasks found in this category")
	return tasks

@router.get("/tasks/priority/{priority}", response_model=List[schemas.TaskOut], tags=["filtering"])
def get_tasks_by_priority(priority: str, db: Session = Depends(get_db)):
	"""Get all tasks with a specific priority"""
	tasks = crud.get_tasks_by_priority(db, priority)
	if not tasks:
		raise HTTPException(status_code=404, detail="No tasks found with this priority")
	return tasks

# ==================== TASK LOGS ====================

@router.get("/tasks/{task_id}/logs", response_model=List[schemas.TaskLogOut], tags=["logging"])
def get_task_logs(task_id: int, limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
	"""Get execution logs for a task"""
	# Verify task exists
	task = crud.get_task(db, task_id)
	if not task:
		raise HTTPException(status_code=404, detail="Task not found")
	return crud.get_task_logs(db, task_id, limit)

@router.post("/tasks/{task_id}/log", response_model=schemas.TaskLogOut, status_code=status.HTTP_201_CREATED, tags=["logging"])
def create_task_log(task_id: int, log: schemas.TaskLogBase, db: Session = Depends(get_db)):
	"""Create a log entry for a task"""
	task = crud.get_task(db, task_id)
	if not task:
		raise HTTPException(status_code=404, detail="Task not found")
	return crud.create_log(db, log)

# ==================== WORKFLOWS ====================

@router.post("/workflows", response_model=schemas.TaskWorkflowOut, status_code=status.HTTP_201_CREATED, tags=["workflows"])
def create_workflow(workflow: schemas.TaskWorkflowCreate, db: Session = Depends(get_db)):
	"""Create a task workflow"""
	return crud.create_workflow(db=db, workflow=workflow)

@router.get("/workflows", response_model=List[schemas.TaskWorkflowOut], tags=["workflows"])
def list_workflows(skip: int = Query(0, ge=0), limit: int = Query(100, ge=1, le=1000), db: Session = Depends(get_db)):
	"""List all workflows"""
	return crud.get_workflows(db, skip=skip, limit=limit)

@router.get("/workflows/{workflow_id}", response_model=schemas.TaskWorkflowOut, tags=["workflows"])
def get_workflow(workflow_id: int, db: Session = Depends(get_db)):
	"""Get a specific workflow"""
	workflow = crud.get_workflow(db, workflow_id)
	if not workflow:
		raise HTTPException(status_code=404, detail="Workflow not found")
	return workflow

@router.delete("/workflows/{workflow_id}", status_code=status.HTTP_204_NO_CONTENT, tags=["workflows"])
def delete_workflow(workflow_id: int, db: Session = Depends(get_db)):
	"""Delete a workflow"""
	deleted = crud.delete_workflow(db, workflow_id)
	if not deleted:
		raise HTTPException(status_code=404, detail="Workflow not found")

# ==================== ANALYTICS ====================

@router.get("/statistics", response_model=schemas.TaskStatistics, tags=["analytics"])
def get_statistics(db: Session = Depends(get_db)):
	"""Get overall task statistics"""
	stats = crud.get_task_statistics(db)
	return schemas.TaskStatistics(**stats)

