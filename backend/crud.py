#Database access logic

from sqlalchemy.orm import Session
from models import Todo
from schemas import TodoCreate, TodoUpdate
from datetime import date

def get_todos(db: Session, skip: int=0, limit: int=100):
	return db.query(Todo).offset(skip).limit(limit).all()

def get_todo(db: Session, todo_id: int):
	return db.query(Todo).filter(Todo.id == todo_id).first()

def create_todo(db: Session, todo: TodoCreate):
	db_todo = Todo(**todo.model_dump(), created_at=date.today())
	db.add(db_todo)
	db.commit()
	db.refresh(db_todo)
	return db_todo

def update_todo(db: Session, todo_id: int, todo: TodoUpdate):
	db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
	if not db_todo:
		return None
	for key, value in todo.dict(exclude_unset=True).items():
		setattr(db_todo, key, value)
	db.commit()
	db.refresh(db_todo)
	return db_todo

def delete_todo(db: Session, todo_id: int):
	db_todo = db.query(Todo).filter(Todo.id == todo_id).first()
	if not db_todo:
		return None
	db.delete(db_todo)
	db.commit()
	return db_todo


