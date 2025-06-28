from fastapi import FastAPI, HTTPException
from pydantic import BaseModel
from typing import List
from fastapi.middleware.cors import CORSMiddleware
from datetime import date, datetime

app = FastAPI()

app.add_middleware(CORSMiddleware, allow_origins=["http://localhost:3000"], allow_credentials=True, allow_methods=["*"], allow_headers=["*"])



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
todos = []
next_id = 1

@app.get("/todos", response_model=List[TodoItem])
def get_todos():
	return todos

@app.post("/todos", response_model=TodoItem)
def create_todo(item: TodoItemCreate):
	global next_id
	todo = TodoItem(id=next_id, title=item.title, completed=item.completed, due_date=item.due_date, category=item.category)
	#item.id = next_id
	next_id += 1
	todos.append(todo)
	return todo

@app.put("/todos/{todo_id}", response_model=TodoItem)
def update_todo(todo_id: int, item: TodoItemCreate):
        print("Current Todos:", todos)
        print("Looking for ID:", todo_id)
        for i, todo in enumerate(todos):
                if todo.id == todo_id:
                    completed_now = item.completed and not todo.completed
                    updated = TodoItem(id=todo_id, title=item.title, completed=item.completed, due_date=item.due_date, category=item.category, completed_at=datetime.now() if completed_now else todo.completed_at)
                    todos[i] = updated
                    return updated

        raise HTTPException(status_code=404, detail="Todo not found")


@app.delete("/todos/{todo_id}")
def delete_todo(todo_id: int):
	for i, todo in enumerate(todos):
		if todo.id == todo_id:
			todos.pop(i)
			return {"detail": "Todo Deleted"}
	return HTTPException(status_code=404, detail="Todo not found")




