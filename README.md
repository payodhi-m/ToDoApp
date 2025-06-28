# Full-Stack Todo App (React + FastAPI)

A simple and powerful full-stack Todo list application built using **React** for the frontend and **FastAPI** for the backend.

## Phase 1 Features Implemented

### Core Features:
- Create, update, delete tasks
- Mark tasks as complete/incomplete
- Task persistence using in-memory store (can be upgraded to DB later)

### Filtering & Searching 
- Filter tasks by:
  - All
  - Active (incomplete)
  - Completed
- Real-time search by task title

### Due Date
- Add optional due dates while creating/editing tasks
- Overdue tasks highlighted in **red**
- Due tasks (still pending) shown in **gray**
- Completed tasks ignore due date color logic

### Progress Bar
- Visual indication of total % of tasks completed
- Clean progress bar with smooth animation

### Task Completed Today
- A counter showing how many tasks were marked completed **today**

### Categories / Labels
- Add category while creating/editing a task
- Filter tasks by category via dropdown


## Phase 2: Backend & Data Persistence
- Integrated SQLite Database using SQLAlchemy ORM
- Separated concerns: `models.py`, `schemas.py`, `crud.py`
- Alembic for database migration
- Used Pydantic v2 
- Improved error handling
- Wrote test cases using `pytest` and FastAPI's TestClient


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
├── backe
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


## Instructions to Run the code
### Backend (FastAPI)

1. Create and activate virtual environment:

```bash
python -m venv venv
source venv/bin/activate  # Windows: venv\Scripts\activate

2. Install Dependencies:
pip install fastapi uvicorn

3. Run FastAPI server:
uvicorn main:app --reload

Backend will be running on: http://127.0.0.1:8000

4. To run tests:
python -m pytest

5. To apply DB migration:
alembic upgrade head

### Frontend (React)
1. Navigate to frontend folder
cd frontend

2. Install React dependencies
npm install

3. Start the development server
npm start

Frontend will be running on: http://localhost:3000

```

### Upcoming (Phase 3 Plan)

User Authentication + JWT-based login system

### Contributing
Suggestions, bug reports, and contributions are welcome! Feel free to fork the repo and raise a pull request

