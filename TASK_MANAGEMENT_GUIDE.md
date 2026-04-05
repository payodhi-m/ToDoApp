# Simple TODO App - User Guide

## Overview

This is a user-friendly task management application for organizing daily tasks, tracking progress, and boosting productivity. Built with React frontend and FastAPI backend.

## Getting Started

### Starting the Application

**Backend:**
```bash
cd backend
source venv/bin/activate
python -m uvicorn main:app --reload
```
Backend runs on: **http://127.0.0.1:8000**

**Frontend:**
```bash
cd frontend
npm start
```
Frontend opens at: **http://localhost:3000**

## Main Features

### 1. Creating Tasks
Click **"+ Add New Task"** to open the task creation form:
- **Task Title** (required) - What needs to be done
- **Description** (optional) - Additional details
- **Due Date** (optional) - When the task needs to be done
- **Category** (optional) - Organize by type (work, personal, shopping, etc.)
- **Priority** - Low, Medium, High, or Critical
- **Estimated Hours** (optional) - How long you think it will take
- **Tags** (optional) - Comma-separated keywords

Click **"Create Task"** to add it to your list.

### 2. Managing Tasks

#### Completing Tasks
Check the checkbox next to a task to mark it complete. Completed tasks move to a grayish background.

#### Editing Tasks
Click **"✎ Edit"** to modify task details. Update any field and click **"Save"**.

#### Deleting Tasks
Click **"🗑 Delete"** to remove a task permanently.

### 3. View Navigation

The navigation tabs filter your tasks by view:

- **📅 Today** - Tasks due today only (incomplete)
- **📆 Upcoming** - Incomplete tasks due in next 7 days  
- **⚠️ Overdue** - Incomplete tasks past their due date
- **📋 All Tasks** - All incomplete tasks
- **✅ Completed** - All tasks you've finished
- **🗓️ Agenda** - Pick a date to see tasks for that day

### 4. Filtering

**By Category:**
- Select from "All Categories" dropdown
- Shows only tasks in the selected category
- Categories are created automatically when you set a task's category

**By Priority:**
- Filter by Critical, High, Medium, or Low
- Combined with category filter for detailed views

## Task Information

### Priority Levels

| Priority | Color | Usage |
|----------|-------|-------|
| Critical | 🔴 Red | Urgent, time-sensitive tasks |
| High | 🟠 Orange | Important, needs attention soon |
| Medium | 🟡 Yellow | Standard daily tasks |
| Low | ⚪ Gray | Background, flexible timing |

### Task Metadata

Each task can display:
- **📂 Category** - Custom category label
- **📅 Due Date** - Deadline for the task
- **⏱️ Estimated Hours** - Time estimate (e.g., "2h")
- **✓ Time Spent** - Actual hours spent
- **#Tags** - Multiple tags for organization

### Status Indicators

- ✓ Checked box = Completed task
- **⚠️ Overdue** badge = Past due and incomplete
- **✓ Done** badge = Completed task

## Statistics Dashboard

The stats section at the top shows:
- **Total Tasks** - All tasks in your system
- **Completed** - Tasks you've finished
- **Pending** - Incomplete tasks
- **Completion Rate** - Percentage of completed tasks

## Color-Coded Design

The app uses intuitive colors:
- **Purple gradient** (#667eea → #764ba2) - Primary theme
- **Yellow (#ffc107)** - Medium priority
- **Orange (#fd7e14)** - High priority  
- **Red (#dc3545)** - Critical priority/Overdue
- **Green (#28a745)** - Completed/Success

## Tips & Tricks

### Organizing Tasks
1. Use **Categories** for project or area grouping (Work, Home, Shopping)
2. Use **Tags** for cross-cutting concerns (#urgent, #bug, #feature)
3. Use **Priority** levels to focus on what matters most

### Productivity Tips
1. Check **"Today"** tab each morning to see your daily tasks
2. Use **Estimated Hours** to manage workload
3. Review **"Completed"** tab to see your progress
4. Update due dates to keep priorities accurate
5. Use **Overdue** tab to catch tasks that need attention

### Calendar Planning
Use the **Agenda** view to:
- Plan tasks for specific dates
- See your schedule at a glance
- Find available time slots

## Error Handling

If you see an error message:
1. Check that the backend server is running
2. Verify the API URL is correct (http://127.0.0.1:8000)
3. Check browser console (F12) for detailed errors
4. Try refreshing the page

## API Reference

For developers integrating with the backend:

### Task CRUD
```
GET    /api/tasks                 - List all tasks
POST   /api/tasks                 - Create task
GET    /api/tasks/{id}            - Get task
PUT    /api/tasks/{id}            - Update task
DELETE /api/tasks/{id}            - Delete task
```

### Quick Views
```
GET    /api/tasks/view/today      - Today's tasks
GET    /api/tasks/view/upcoming   - Next 7 days
GET    /api/tasks/view/overdue    - Overdue tasks
GET    /api/tasks/view/pending    - All incomplete
GET    /api/tasks/view/completed  - Completed history
```

### Organization
```
GET    /api/categories            - All categories
GET    /api/tasks/category/{name} - Category filter
GET    /api/agenda/date/{date}    - Date view (YYYY-MM-DD)
GET    /api/agenda/range          - Date range view
```

### Analytics
```
GET    /api/stats                 - Statistics
```

## Task Data Structure

```json
{
  "id": 1,
  "title": "Complete project report",
  "description": "Finish Q1 analysis and send to team",
  "priority": "high",
  "due_date": "2025-04-10",
  "category": "work",
  "tags": ["reporting", "quarterly"],
  "completed": false,
  "completed_at": null,
  "estimated_hours": 3.0,
  "time_spent_hours": 1.5,
  "is_recurring": false,
  "recurrence_pattern": null,
  "created_at": "2025-04-03T10:30:00",
  "updated_at": "2025-04-03T14:00:00"
}
```

## Keyboard Shortcuts

- **Tab** - Navigate between form fields
- **Enter** - Submit form (when in form)

## Browser Compatibility

Works best in:
- Chrome/Edge 90+
- Firefox 88+
- Safari 14+

## Support

For issues:
1. Check the browser console (F12)
2. Verify backend is running
3. Check CORS settings if requests fail
4. Try clearing cache and refreshing

## Future Features

Possible enhancements:
- Recurring tasks
- Task notifications
- Color-coding by category
- Drag-and-drop reordering
- Advanced search
- Task templates
- Team collaboration
- Mobile app
- Dark mode

**Version**: 1.0.0  
**Last Updated**: 2025-04-03  
**Status**: Production Ready
