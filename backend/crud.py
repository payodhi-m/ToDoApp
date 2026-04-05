#Database CRUD operations for TODO App

from sqlalchemy.orm import Session
from sqlalchemy import desc
from models import Task, TaskPriority
from schemas import TaskCreate, TaskUpdate
from datetime import datetime, date, timedelta
from typing import Optional, List

# ==================== TASK OPERATIONS ====================

def get_tasks(db: Session, skip: int = 0, limit: int = 100, priority: Optional[str] = None, category: Optional[str] = None):
	"""Retrieve tasks with optional filters"""
	query = db.query(Task)
	if priority:
		query = query.filter(Task.priority == priority)
	if category:
		query = query.filter(Task.category == category)
	return query.order_by(desc(Task.priority), desc(Task.due_date)).offset(skip).limit(limit).all()

def get_task(db: Session, task_id: int):
	"""Get a specific task by ID"""
	return db.query(Task).filter(Task.id == task_id).first()

def create_task(db: Session, task: TaskCreate):
	"""Create a new task"""
	db_task = Task(
		title=task.title,
		description=task.description,
		priority=task.priority.value if task.priority else TaskPriority.MEDIUM.value,
		due_date=task.due_date,
		category=task.category,
		tags=task.tags,
		estimated_hours=task.estimated_hours,
		is_recurring=task.is_recurring,
		recurrence_pattern=task.recurrence_pattern,
		created_at=datetime.utcnow(),
		updated_at=datetime.utcnow()
	)
	db.add(db_task)
	db.commit()
	db.refresh(db_task)
	return db_task

def update_task(db: Session, task_id: int, task: TaskUpdate):
	"""Update a task"""
	db_task = db.query(Task).filter(Task.id == task_id).first()
	if not db_task:
		return None
	
	update_data = task.dict(exclude_unset=True)
	if "priority" in update_data and update_data["priority"]:
		update_data["priority"] = update_data["priority"].value
	
	# If marking as completed, set completion timestamp
	if "completed" in update_data and update_data["completed"] and not db_task.completed_at:
		update_data["completed_at"] = datetime.utcnow()
	
	update_data["updated_at"] = datetime.utcnow()
	
	for key, value in update_data.items():
		setattr(db_task, key, value)
	
	db.commit()
	db.refresh(db_task)
	return db_task

def delete_task(db: Session, task_id: int):
	"""Delete a task"""
	db_task = db.query(Task).filter(Task.id == task_id).first()
	if not db_task:
		return None
	db.delete(db_task)
	db.commit()
	return db_task

def get_today_tasks(db: Session):
	"""Get all tasks for today"""
	today = date.today()
	return db.query(Task).filter(Task.due_date == today).order_by(desc(Task.priority)).all()

def get_overdue_tasks(db: Session):
	"""Get overdue incomplete tasks"""
	return db.query(Task).filter(
		Task.due_date < date.today(),
		Task.completed == False
	).order_by(Task.due_date).all()

def get_upcoming_tasks(db: Session, days: int = 7):
	"""Get tasks due in the next N days"""
	today = date.today()
	future_date = today + timedelta(days=days)
	return db.query(Task).filter(
		Task.due_date >= today,
		Task.due_date <= future_date,
		Task.completed == False
	).order_by(Task.due_date).all()

def get_pending_tasks(db: Session):
	"""Get all incomplete tasks"""
	return db.query(Task).filter(Task.completed == False).order_by(desc(Task.priority), Task.due_date).all()

def get_completed_tasks(db: Session, skip: int = 0, limit: int = 100):
	"""Get completed tasks"""
	return db.query(Task).filter(Task.completed == True).order_by(desc(Task.completed_at)).offset(skip).limit(limit).all()

def get_tasks_by_category(db: Session, category: str, skip: int = 0, limit: int = 100):
	"""Get tasks by category"""
	return db.query(Task).filter(Task.category == category).order_by(desc(Task.priority)).offset(skip).limit(limit).all()

def get_categories(db: Session):
	"""Get all distinct categories"""
	categories = db.query(Task.category).distinct().filter(Task.category.isnot(None)).all()
	return [c[0] for c in categories]

def get_agenda_for_date(db: Session, target_date: date):
	"""Get all tasks for a specific date"""
	return db.query(Task).filter(Task.due_date == target_date).order_by(desc(Task.priority)).all()

def get_agenda_range(db: Session, start_date: date, end_date: date):
	"""Get all tasks in a date range"""
	return db.query(Task).filter(
		Task.due_date >= start_date,
		Task.due_date <= end_date
	).order_by(Task.due_date, desc(Task.priority)).all()

# ==================== STATISTICS ====================

def get_task_statistics(db: Session):
	"""Get overall task statistics"""
	total = db.query(Task).count()
	completed = db.query(Task).filter(Task.completed == True).count()
	pending = db.query(Task).filter(Task.completed == False).count()
	
	completion_rate = (completed / total * 100) if total > 0 else 0
	
	# Time tracking
	all_tasks = db.query(Task).all()
	estimated_hours = sum(t.estimated_hours or 0 for t in all_tasks)
	spent_hours = sum(t.time_spent_hours or 0 for t in all_tasks)
	
	# Priority distribution
	priority_dist = {}
	for priority in TaskPriority:
		count = db.query(Task).filter(Task.priority == priority.value).count()
		priority_dist[priority.value] = count
	
	# Category distribution
	category_dist = {}
	categories = get_categories(db)
	for cat in categories:
		count = db.query(Task).filter(Task.category == cat).count()
		category_dist[cat] = count
	
	return {
		"total_tasks": total,
		"completed_tasks": completed,
		"pending_tasks": pending,
		"completion_rate": round(completion_rate, 2),
		"total_estimated_hours": estimated_hours,
		"total_spent_hours": spent_hours,
		"tasks_by_priority": priority_dist,
		"tasks_by_category": category_dist
	}

