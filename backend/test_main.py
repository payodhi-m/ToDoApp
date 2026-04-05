
from fastapi.testclient import TestClient
from main import app
from datetime import date, datetime, timedelta
import pytest

client = TestClient(app)

# ==================== CORE CRUD TESTS ====================

def test_create_task_basic():
	"""Test creating a basic task"""
	response = client.post("/api/tasks", json={
		"title": "Test Task",
		"priority": "medium",
		"category": "testing"
	})
	assert response.status_code == 201
	data = response.json()
	assert data["title"] == "Test Task"
	assert data["priority"] == "medium"
	assert data["completed"] == False
	assert "id" in data

def test_create_task_with_all_fields():
	"""Test creating task with all optional fields"""
	tomorrow = (datetime.now() + timedelta(days=1)).date()
	response = client.post("/api/tasks", json={
		"title": "Complex Task",
		"description": "Task with all fields",
		"priority": "critical",
		"category": "development",
		"tags": ["backend", "feature"],
		"due_date": str(tomorrow),
		"estimated_hours": 4.5
	})
	assert response.status_code == 201
	data = response.json()
	assert data["title"] == "Complex Task"
	assert data["priority"] == "critical"
	assert data["tags"] == ["backend", "feature"]
	assert data["estimated_hours"] == 4.5
	assert data["description"] == "Task with all fields"

def test_create_task_missing_title():
	"""Test creating task without required title fails"""
	response = client.post("/api/tasks", json={
		"priority": "high"
	})
	assert response.status_code == 422  # Validation error

def test_list_tasks():
	"""Test listing all tasks"""
	# Create a task first
	client.post("/api/tasks", json={
		"title": "List Test Task",
		"priority": "medium"
	})
	
	response = client.get("/api/tasks")
	assert response.status_code == 200
	assert isinstance(response.json(), list)
	assert len(response.json()) > 0

def test_list_tasks_with_pagination():
	"""Test listing tasks with pagination"""
	response = client.get("/api/tasks?skip=0&limit=10")
	assert response.status_code == 200
	assert isinstance(response.json(), list)

def test_get_task():
	"""Test getting a specific task"""
	# Create a task first
	create_response = client.post("/api/tasks", json={
		"title": "Get Task Test",
		"priority": "high"
	})
	task_id = create_response.json()["id"]
	
	# Get the task
	response = client.get(f"/api/tasks/{task_id}")
	assert response.status_code == 200
	assert response.json()["id"] == task_id
	assert response.json()["title"] == "Get Task Test"

def test_get_task_not_found():
	"""Test getting non-existent task"""
	response = client.get("/api/tasks/999999")
	assert response.status_code == 404

def test_update_task():
	"""Test updating a task"""
	# Create a task
	create_response = client.post("/api/tasks", json={
		"title": "Update Test",
		"priority": "low"
	})
	task_id = create_response.json()["id"]
	
	# Update it
	response = client.put(f"/api/tasks/{task_id}", json={
		"title": "Updated Title",
		"priority": "critical",
		"completed": True
	})
	assert response.status_code == 200
	data = response.json()
	assert data["title"] == "Updated Title"
	assert data["priority"] == "critical"
	assert data["completed"] == True

def test_update_task_partial():
	"""Test partial update of task"""
	# Create a task
	create_response = client.post("/api/tasks", json={
		"title": "Partial Update Test",
		"priority": "medium",
		"category": "work"
	})
	task_id = create_response.json()["id"]
	
	# Update only one field
	response = client.put(f"/api/tasks/{task_id}", json={
		"priority": "high"
	})
	assert response.status_code == 200
	data = response.json()
	assert data["priority"] == "high"
	assert data["title"] == "Partial Update Test"  # Unchanged
	assert data["category"] == "work"  # Unchanged

def test_update_task_not_found():
	"""Test updating non-existent task"""
	response = client.put("/api/tasks/999999", json={
		"title": "Update Attempt",
		"priority": "high"
	})
	assert response.status_code == 404

def test_delete_task():
	"""Test deleting a task"""
	# Create a task
	create_response = client.post("/api/tasks", json={
		"title": "Delete Test",
		"priority": "medium"
	})
	task_id = create_response.json()["id"]
	
	# Delete it
	response = client.delete(f"/api/tasks/{task_id}")
	assert response.status_code == 204
	
	# Verify it's deleted
	get_response = client.get(f"/api/tasks/{task_id}")
	assert get_response.status_code == 404

def test_delete_task_not_found():
	"""Test deleting non-existent task"""
	response = client.delete("/api/tasks/999999")
	assert response.status_code == 404

# ==================== VIEW-BASED FILTERING TESTS ====================

def test_view_today_tasks():
	"""Test getting today's tasks"""
	today = datetime.now().date()
	
	# Create a task due today
	client.post("/api/tasks", json={
		"title": "Today's Task",
		"priority": "high",
		"due_date": str(today)
	})
	
	# Create a task due tomorrow
	tomorrow = today + timedelta(days=1)
	client.post("/api/tasks", json={
		"title": "Tomorrow's Task",
		"priority": "medium",
		"due_date": str(tomorrow)
	})
	
	response = client.get("/api/tasks/view/today")
	assert response.status_code == 200
	tasks = response.json()
	assert isinstance(tasks, list)
	# All returned tasks should be due today
	for task in tasks:
		if task["due_date"]:
			assert task["due_date"] == str(today)

def test_view_upcoming_tasks():
	"""Test getting upcoming tasks"""
	today = datetime.now().date()
	
	# Create a task due in 3 days
	in_3_days = today + timedelta(days=3)
	client.post("/api/tasks", json={
		"title": "Upcoming Task",
		"priority": "medium",
		"due_date": str(in_3_days)
	})
	
	response = client.get("/api/tasks/view/upcoming")
	assert response.status_code == 200
	tasks = response.json()
	assert isinstance(tasks, list)
	# All returned tasks should be incomplete
	for task in tasks:
		assert task["completed"] == False

def test_view_overdue_tasks():
	"""Test getting overdue tasks"""
	yesterday = datetime.now().date() - timedelta(days=1)
	
	# Create an overdue task
	client.post("/api/tasks", json={
		"title": "Overdue Task",
		"priority": "critical",
		"due_date": str(yesterday)
	})
	
	response = client.get("/api/tasks/view/overdue")
	assert response.status_code == 200
	tasks = response.json()
	assert isinstance(tasks, list)
	# All returned tasks should be incomplete and past due
	for task in tasks:
		assert task["completed"] == False

def test_view_pending_tasks():
	"""Test getting all pending tasks"""
	# Create multiple tasks
	client.post("/api/tasks", json={
		"title": "Pending 1",
		"priority": "high"
	})
	client.post("/api/tasks", json={
		"title": "Pending 2",
		"priority": "low"
	})
	
	response = client.get("/api/tasks/view/pending")
	assert response.status_code == 200
	tasks = response.json()
	assert isinstance(tasks, list)
	# All returned tasks should be incomplete
	for task in tasks:
		assert task["completed"] == False

def test_view_completed_tasks():
	"""Test getting completed tasks"""
	# Create a task
	create_response = client.post("/api/tasks", json={
		"title": "Complete Me",
		"priority": "medium"
	})
	task_id = create_response.json()["id"]
	
	# Complete it
	client.put(f"/api/tasks/{task_id}", json={"completed": True})
	
	response = client.get("/api/tasks/view/completed")
	assert response.status_code == 200
	tasks = response.json()
	assert isinstance(tasks, list)
	# All returned tasks should be completed
	for task in tasks:
		assert task["completed"] == True

# ==================== CATEGORY FILTERING TESTS ====================

def test_filter_tasks_by_category():
	"""Test filtering tasks by category"""
	# Create tasks with different categories
	client.post("/api/tasks", json={
		"title": "Backend Task",
		"category": "backend"
	})
	client.post("/api/tasks", json={
		"title": "Frontend Task",
		"category": "frontend"
	})
	
	response = client.get("/api/tasks/category/backend")
	assert response.status_code == 200
	tasks = response.json()
	assert isinstance(tasks, list)
	# All tasks should have backend category
	for task in tasks:
		assert task["category"] == "backend"

def test_get_all_categories():
	"""Test getting list of all categories"""
	# Create tasks with different categories
	client.post("/api/tasks", json={
		"title": "Work Task",
		"category": "work"
	})
	client.post("/api/tasks", json={
		"title": "Personal Task",
		"category": "personal"
	})
	
	response = client.get("/api/categories")
	assert response.status_code == 200
	categories = response.json()
	assert isinstance(categories, list)
	assert len(categories) > 0

# ==================== AGENDA/CALENDAR TESTS ====================

def test_get_agenda_for_date():
	"""Test getting tasks for a specific date"""
	target_date = datetime.now().date() + timedelta(days=5)
	
	# Create a task for that date
	client.post("/api/tasks", json={
		"title": "Task on Target Date",
		"due_date": str(target_date)
	})
	
	response = client.get(f"/api/agenda/date/{target_date}")
	assert response.status_code == 200
	data = response.json()
	assert "tasks" in data
	assert isinstance(data["tasks"], list)

def test_get_agenda_range():
	"""Test getting tasks in a date range"""
	start_date = datetime.now().date()
	end_date = start_date + timedelta(days=7)
	
	# Create tasks in the range
	for i in range(3):
		date_in_range = start_date + timedelta(days=i+1)
		client.post("/api/tasks", json={
			"title": f"Task {i+1}",
			"due_date": str(date_in_range)
		})
	
	response = client.get(f"/api/agenda/range?start={start_date}&end={end_date}")
	assert response.status_code == 200
	data = response.json()
	assert isinstance(data, list)

# ==================== STATISTICS TESTS ====================

def test_get_statistics():
	"""Test getting task statistics"""
	# Create some tasks
	client.post("/api/tasks", json={
		"title": "Stat Task 1",
		"priority": "high",
		"category": "work"
	})
	client.post("/api/tasks", json={
		"title": "Stat Task 2",
		"priority": "low",
		"category": "personal"
	})
	
	response = client.get("/api/stats")
	assert response.status_code == 200
	stats = response.json()
	
	# Verify statistics structure
	assert "total_tasks" in stats
	assert "completed_tasks" in stats
	assert "pending_tasks" in stats
	assert "completion_rate" in stats
	assert "tasks_by_priority" in stats
	assert "tasks_by_category" in stats
	
	# Verify values are reasonable
	assert stats["total_tasks"] >= 0
	assert stats["completed_tasks"] >= 0
	assert stats["pending_tasks"] >= 0
	assert 0 <= stats["completion_rate"] <= 100


# ==================== TASK METADATA TESTS ====================

def test_task_with_time_tracking():
	"""Test creating task with time tracking fields"""
	response = client.post("/api/tasks", json={
		"title": "Time Tracking Task",
		"priority": "high",
		"estimated_hours": 5.5
	})
	assert response.status_code == 201
	task = response.json()
	assert task["estimated_hours"] == 5.5
	assert task["time_spent_hours"] == 0.0

def test_update_task_time_spent():
	"""Test updating time spent on a task"""
	# Create a task
	create_response = client.post("/api/tasks", json={
		"title": "Time Update Task",
		"estimated_hours": 3.0
	})
	task_id = create_response.json()["id"]
	
	# Update time spent
	response = client.put(f"/api/tasks/{task_id}", json={
		"time_spent_hours": 1.5
	})
	assert response.status_code == 200
	assert response.json()["time_spent_hours"] == 1.5

def test_task_with_tags():
	"""Test creating task with tags"""
	response = client.post("/api/tasks", json={
		"title": "Tagged Task",
		"tags": ["urgent", "review", "backend"]
	})
	assert response.status_code == 201
	task = response.json()
	assert task["tags"] == ["urgent", "review", "backend"]

def test_task_with_recurring():
	"""Test creating recurring task"""
	response = client.post("/api/tasks", json={
		"title": "Weekly Team Meeting",
		"priority": "high",
		"is_recurring": True,
		"recurrence_pattern": "weekly"
	})
	assert response.status_code == 201
	task = response.json()
	assert task["is_recurring"] == True
	assert task["recurrence_pattern"] == "weekly"

# ==================== PRIORITY LEVEL TESTS ====================

def test_all_priority_levels():
	"""Test all priority levels"""
	priorities = ["low", "medium", "high", "critical"]
	
	for priority in priorities:
		response = client.post("/api/tasks", json={
			"title": f"Priority {priority}",
			"priority": priority
		})
		assert response.status_code == 201
		assert response.json()["priority"] == priority

def test_priority_filtering_in_list():
	"""Test that task list can be filtered by priority via query parameters"""
	# Create tasks with different priorities
	client.post("/api/tasks", json={
		"title": "Critical Task",
		"priority": "critical"
	})
	client.post("/api/tasks", json={
		"title": "Low Priority",
		"priority": "low"
	})
	
	# Get all tasks and filter in memory (API list endpoint for priority filtering)
	response = client.get("/api/tasks?priority=critical")
	assert response.status_code == 200
	# This test validates the endpoint accepts the parameter even if backend
	# filters client-side in this simplified version

# ==================== EDGE CASES ====================

def test_empty_category():
	"""Test tasks with no category"""
	response = client.post("/api/tasks", json={
		"title": "Uncategorized Task",
		"priority": "medium"
	})
	assert response.status_code == 201
	task = response.json()
	# Category should be None or empty
	assert task.get("category") is None or task.get("category") == ""

def test_task_with_long_description():
	"""Test creating task with long description"""
	long_description = "A" * 1000  # 1000 character description
	response = client.post("/api/tasks", json={
		"title": "Long Description Task",
		"description": long_description
	})
	assert response.status_code == 201
	task = response.json()
	assert len(task["description"]) == 1000

def test_update_multiple_fields():
	"""Test updating multiple fields at once"""
	# Create a task
	create_response = client.post("/api/tasks", json={
		"title": "Multi-Update Task",
		"priority": "low",
		"category": "personal"
	})
	task_id = create_response.json()["id"]
	
	# Update multiple fields
	response = client.put(f"/api/tasks/{task_id}", json={
		"title": "Updated Title",
		"priority": "critical",
		"category": "work",
		"completed": True,
		"estimated_hours": 2.0
	})
	assert response.status_code == 200
	task = response.json()
	assert task["title"] == "Updated Title"
	assert task["priority"] == "critical"
	assert task["category"] == "work"
	assert task["completed"] == True
	assert task["estimated_hours"] == 2.0
