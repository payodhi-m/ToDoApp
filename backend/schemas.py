# Contains only Pydantic models

from pydantic import BaseModel, ConfigDict
from typing import Optional
from datetime import date

class TodoBase(BaseModel):
	title: str
	completed: bool = False
	due_date: Optional[date] = None
	category: Optional[str] = None

	model_config = ConfigDict(from_attributes=True)

class TodoCreate(TodoBase):
	pass

class TodoUpdate(TodoBase):
	pass

class TodoOut(TodoBase):
	id: int
	created_at: Optional[date]

	'''class Config:
		orm_mode = True'''


