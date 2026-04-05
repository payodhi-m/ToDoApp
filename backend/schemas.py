# TODO App Schemas

from pydantic import BaseModel, ConfigDict, Field
from typing import Optional, List
from datetime import date, datetime
from enum import Enum

class TaskPriority(str, Enum):
	LOW = "low"
	MEDIUM = "medium"
	HIGH = "high"
	CRITICAL = "critical"

# Task Schemas
class TaskBase(BaseModel):
	title: str = Field(..., min_length=1, max_length=255)
	description: Optional[str] = None
	priority: TaskPriority = TaskPriority.MEDIUM
	due_date: Optional[date] = None
	category: Optional[str] = None
	tags: Optional[List[str]] = None
	estimated_hours: Optional[float] = None
	is_recurring: bool = False
	recurrence_pattern: Optional[str] = None  # daily, weekly, monthly

	model_config = ConfigDict(from_attributes=True)

class TaskCreate(TaskBase):
	pass

class TaskUpdate(BaseModel):
	title: Optional[str] = None
	description: Optional[str] = None
	priority: Optional[TaskPriority] = None
	due_date: Optional[date] = None
	category: Optional[str] = None
	tags: Optional[List[str]] = None
	completed: Optional[bool] = None
	estimated_hours: Optional[float] = None
	time_spent_hours: Optional[float] = None
	is_recurring: Optional[bool] = None
	recurrence_pattern: Optional[str] = None

	model_config = ConfigDict(from_attributes=True)

class TaskOut(TaskBase):
	id: int
	completed: bool
	time_spent_hours: float
	created_at: Optional[datetime]
	updated_at: Optional[datetime]
	completed_at: Optional[datetime]

	model_config = ConfigDict(from_attributes=True)

# Statistics
class TaskStatistics(BaseModel):
	total_tasks: int
	completed_tasks: int
	pending_tasks: int
	completion_rate: float
	tasks_by_priority: dict
	tasks_by_category: dict
	total_estimated_hours: float
	total_spent_hours: float

class AgendaItem(BaseModel):
	"""Agenda item for calendar view"""
	date: date
	tasks: List[TaskOut]
	completed_count: int
	total_count: int
