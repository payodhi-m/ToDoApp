# Simple TODO App (React + FastAPI)

A clean and user-friendly task management application built with **React** (frontend) and **FastAPI** (backend). Perfect for organizing daily tasks, managing priorities, and tracking productivity.

## Features

### Task Management
- ✅ Create, read, update, and delete tasks
- ✅ Mark tasks as complete/incomplete
- ✅ Task persistence with SQLite database

### Task Organization
- 📊 **Priority Levels** - Low, Medium, High, Critical
- 📂 **Categories** - Organize tasks by custom categories
- 🏷️ **Tags** - Flexible tagging system for cross-cutting concerns
- ⏱️ **Time Tracking** - Estimate hours and track actual time spent

### Smart Views
- **Today** - Tasks due today only
- **Upcoming** - Tasks due in the next 7 days
- **Overdue** - Past-due incomplete tasks
- **All Tasks** - Complete task list
- **Completed** - Historical completed tasks
- **Agenda** - Calendar view for any date

### Dashboard & Statistics
- 📈 Stats cards showing total, completed, pending, and completion rate
- 🎯 Quick navigation tabs for filtering
- 🔍 Filter by category and priority

### Backend & Data Persistence
- SQLite database with SQLAlchemy ORM
- Clean architecture: `models.py`, `schemas.py`, `crud.py`
- FastAPI with comprehensive REST API
- Pydantic v2 for data validation
- Proper error handling and logging


## Tech Stack

| Layer     | Technology  |
|-----------|-------------|
| Frontend  | React (JavaScript) |
| Backend   | FastAPI (Python) |
| Styling   | CSS Modules (basic styles) |
| API Calls | REST using `fetch()` |

-----

## Project Structure

project-root/
│
├── backend/
 ├── main.py
 ├── models.py
 ├── schemas.py
 ├── crud.py
 ├── database.py
 ├── alembic/
 ├── .env
 └── test_main.py
│
├frontend/
│ ├── app.js # Main React app
│ ├── TodoItem.js # Component for each todo
│ ├── index.css # Styling for progress bar, filters, inputs
│ └── ...
│
└── README.md


## Quick Start

### Backend Setup

1. Navigate to backend directory:
```bash
cd backend
```

2. Create and activate virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate
```

3. Install dependencies:
```bash
pip install -r requirement.txt
```

4. Run FastAPI server:
```bash
uvicorn main:app --reload
```

Backend will be running on: **http://127.0.0.1:8000**

### Frontend Setup

1. Navigate to frontend directory:
```bash
cd frontend
```

2. Install dependencies:
```bash
npm install
```

3. Start development server:
```bash
npm start
```

Frontend will open at **http://localhost:3000**

## API Documentation

Once the backend is running, visit **http://127.0.0.1:8000/docs** for interactive API documentation (Swagger UI).


### Contributing
Suggestions, bug reports, and contributions are welcome! Feel free to fork the repo and raise a pull request

