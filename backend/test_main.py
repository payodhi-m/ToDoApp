
from fastapi.testclient import TestClient
from main import app

client = TestClient(app)

def test_create_todo():
	response = client.post("/todos", json={
		"title": "Test Task",
		"completed": False,
		"due_date": None, 
		"category": "test",
	})
	assert response.status_code == 201
	assert response.json()["title"] == "Test Task"

def test_get_todos():
	response = client.get("/todos")
	assert response.status_code == 200
	assert isinstance(response.json(), list)

def test_update_todo_not_found():
	response = client.put("/todos/999", json={
		"title": "Update Attempt",
		"completed": True,
		"due_date": None,
		"category": "test"
	})

	assert response.status_code == 404
	assert response.json()["detail"] == "Todo not found"

def test_delete_todo_not_found():
	response = client.delete("/todos/999")
	assert response.status_code == 404
