from fastapi import FastAPI, HTTPException, Depends, status
from sqlalchemy.orm import Session
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime
import models
import crud
import schemas
from database import engine, Base, SessionLocal


app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])

models.Base.metadata.create_all(bind=engine)


#Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()


#Pydantic model for TODO items
class TodoItemCreate(BaseModel):
	title: str
	completed: bool = False
	due_date: date | None = None
	category: str | None = None

class TodoItem(TodoItemCreate):
	id: int
	completed_at: datetime | None = None
	# title: str
	# completed: bool = False

#In memory storage (simple list)
#todos = []
next_id = 1

@app.get("/todos", response_model=list[schemas.TodoOut])
def read_todos(skip: int=0, limit: int=100, db: Session = Depends(get_db)):
	return crud.get_todos(db, skip=skip, limit=limit)

@app.post("/todos", response_model=schemas.TodoOut, status_code=status.HTTP_201_CREATED)
def create_todo(todo: schemas.TodoCreate, db: Session = Depends(get_db)):
	'''global next_id
	todo = TodoItem(id=next_id, title=item.title, completed=item.completed, due_date=item.due_date, category=item.category)
	#item.id = next_id
	next_id += 1
	todos.append(todo)
	return todo'''
	return crud.create_todo(db=db, todo=todo)

@app.get("/todo/{todo_id}", response_model=schemas.TodoOut)
def read_todo(todo_id: int, db: Session = Depends(get_db)):
	db_todo = crud.get_todo(db, todo_id)
	if db_todo is None:
		raise HTTPException(status_code=404, detail="Todo not Found")
	return db_todo

@app.put("/todos/{todo_id}", response_model=schemas.TodoOut)
def update_todo(todo_id: int, todo: schemas.TodoUpdate, db: Session = Depends(get_db)):
        '''print("Current Todos:", todos)
        print("Looking for ID:", todo_id)
        for i, todo in enumerate(todos):
                if todo.id == todo_id:
                    completed_now = item.completed and not todo.completed
                    updated = TodoItem(id=todo_id, title=item.title, completed=item.completed, due_date=item.due_date, category=item.category, completed_at=datetime.now() if completed_now else todo.completed_at)
                    todos[i] = updated
                    return updated

        raise HTTPException(status_code=404, detail="Todo not found")'''

        updated = crud.update_todo(db, todo_id, todo)
        if updated is None:
            raise HTTPException(status_code=404, detail="Todo not found")
        return updated


@app.delete("/todos/{todo_id}", status_code=status.HTTP_204_NO_CONTENT)
def delete_todo(todo_id: int, db: Session = Depends(get_db)):
	'''for i, todo in enumerate(todos):
		if todo.id == todo_id:
			todos.pop(i)
			return {"detail": "Todo Deleted"}
	return HTTPException(status_code=404, detail="Todo not found")'''

	deleted = crud.delete_todo(db, todo_id)
	if deleted is None:
		raise HTTPException(status_code = 404, detail="Todo not found")
	return {"message": "Todo Deleted"}




