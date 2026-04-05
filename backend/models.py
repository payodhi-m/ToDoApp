from sqlalchemy import Column, Integer, String, Boolean, Date, DateTime, Enum, Float, Text, JSON
from database import Base
from datetime import datetime
import enum

class TaskPriority(str, enum.Enum):
	LOW = "low"
	MEDIUM = "medium"
	HIGH = "high"
	CRITICAL = "critical"

class Task(Base):
	__tablename__ = "tasks"

	id = Column(Integer, primary_key=True, index=True)
	title = Column(String, index=True, nullable=False)
	description = Column(Text, nullable=True)
	
	# Status & Priority
	completed = Column(Boolean, default=False, index=True)
	priority = Column(String, default=TaskPriority.MEDIUM.value)
	
	# Dates
	due_date = Column(Date, nullable=True, index=True)
	completed_at = Column(DateTime, nullable=True)
	
	# Organization
	category = Column(String, nullable=True, index=True)
	tags = Column(JSON, nullable=True)  # List of tags for flexible filtering
	
	# Time Management
	estimated_hours = Column(Float, nullable=True)  # Time estimate in hours
	time_spent_hours = Column(Float, default=0.0)  # Actual time spent
	
	# Recurrence
	is_recurring = Column(Boolean, default=False)
	recurrence_pattern = Column(String, nullable=True)  # daily, weekly, monthly
	
	# Timestamps
	created_at = Column(DateTime, default=datetime.utcnow, nullable=True)
	updated_at = Column(DateTime, default=datetime.utcnow, onupdate=datetime.utcnow, nullable=True)

