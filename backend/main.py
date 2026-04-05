from fastapi import FastAPI, Depends
from fastapi.middleware.cors import CORSMiddleware
from sqlalchemy.orm import Session
import models
from database import engine, SessionLocal
from routers import tasks

# Create tables
models.Base.metadata.create_all(bind=engine)

app = FastAPI(
	title="Simple TODO App",
	description="""
	A clean, user-friendly TODO and agenda management application.
	
	## Features
	- **Task Management**: Create, read, update, and delete tasks
	- **Priority Levels**: Organize tasks by priority (Critical, High, Medium, Low)
	- **Due Dates**: Set and track task due dates
	- **Categories**: Organize tasks by categories
	- **Tags**: Add flexible tags for better organization
	- **Time Tracking**: Estimate and track time spent on tasks
	- **Agenda/Calendar View**: View tasks by date range
	- **Quick Views**: Today's tasks, upcoming tasks, overdue tasks, completed tasks
	- **Statistics**: Task completion rates and progress tracking
	- **Recurring Tasks**: Support for recurring tasks (daily, weekly, monthly)
	
	## Task Views
	- **Today**: Tasks due today
	- **Upcoming**: Tasks due in the next 7 days (customizable)
	- **Overdue**: Incomplete tasks past their due date
	- **Pending**: All incomplete tasks
	- **Completed**: All completed tasks
	- **By Category**: Group tasks by category
	- **Agenda**: Calendar-based view of tasks by date range
	
	## API Endpoints
	- `/api/tasks/` - List and create tasks
	- `/api/tasks/{id}` - Get, update, delete specific tasks
	- `/api/tasks/view/today` - Get today's tasks
	- `/api/tasks/view/upcoming` - Get upcoming tasks
	- `/api/tasks/view/overdue` - Get overdue tasks
	- `/api/tasks/view/pending` - Get all incomplete tasks
	- `/api/tasks/view/completed` - Get completed tasks
	- `/api/categories` - List all categories
	- `/api/tasks/category/{category}` - Filter by category
	- `/api/agenda/date/{date}` - Get tasks for a specific date
	- `/api/agenda/range` - Get tasks in a date range
	- `/api/stats` - Get task statistics
	""",
	version="1.0.0"
)

# CORS Middleware
app.add_middleware(
	CORSMiddleware,
	allow_origins=["http://localhost:3000", "http://localhost:3001", "http://127.0.0.1:3000", "http://127.0.0.1:3001"],
	allow_credentials=True,
	allow_methods=["*"],
	allow_headers=["*"]
)

# Include routers
app.include_router(tasks.router)

# Dependency
def get_db():
	db = SessionLocal()
	try:
		yield db
	finally:
		db.close()

# ==================== HEALTH & INFO ENDPOINTS ====================


if __name__ == "__main__":
	import uvicorn
	uvicorn.run(app, host="0.0.0.0", port=8000)