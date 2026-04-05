import React, { useState, useEffect } from "react";
import TodoItem from "./TodoItem";
import "./App.css";
import "./TodoItem.css";

const API_URL = "http://127.0.0.1:8000/api";

function App() {
  const [tasks, setTasks] = useState([]);
  const [view, setView] = useState("today"); // today, upcoming, pending, completed, agenda
  const [showForm, setShowForm] = useState(false);
  
  // Form state
  const [formData, setFormData] = useState({
    title: "",
    description: "",
    due_date: "",
    category: "",
    priority: "medium",
    estimated_hours: "",
    tags: ""
  });
  
  // Filters
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [priorityFilter, setPriorityFilter] = useState("All");
  const [categories, setCategories] = useState([]);
  const [stats, setStats] = useState(null);
  const [agendaDate, setAgendaDate] = useState(new Date().toISOString().split('T')[0]);
  const [loading, setLoading] = useState(false);
  const [error, setError] = useState("");

  useEffect(() => {
    fetchTasks();
    fetchCategories();
    fetchStats();
  }, []);

  async function fetchTasks() {
    try {
      setLoading(true);
      const res = await fetch(`${API_URL}/tasks`);
      if (!res.ok) throw new Error("Failed to fetch tasks");
      const data = await res.json();
      setTasks(Array.isArray(data) ? data : []);
    } catch (error) {
      console.error("Error fetching tasks:", error);
      setError("Failed to load tasks");
    } finally {
      setLoading(false);
    }
  }

  async function fetchCategories() {
    try {
      const res = await fetch(`${API_URL}/categories`);
      if (res.ok) {
        const data = await res.json();
        setCategories(data || []);
      }
    } catch (error) {
      console.error("Error fetching categories:", error);
    }
  }

  async function fetchStats() {
    try {
      const res = await fetch(`${API_URL}/stats`);
      if (res.ok) {
        const data = await res.json();
        setStats(data);
      }
    } catch (error) {
      console.error("Error fetching stats:", error);
    }
  }

  async function addTask(e) {
    e.preventDefault();
    if (!formData.title.trim()) return;

    try {
      const tagsArray = formData.tags
        .split(",")
        .map(tag => tag.trim())
        .filter(tag => tag.length > 0);

      const res = await fetch(`${API_URL}/tasks`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          title: formData.title,
          description: formData.description || null,
          due_date: formData.due_date || null,
          category: formData.category || null,
          priority: formData.priority,
          estimated_hours: formData.estimated_hours ? parseFloat(formData.estimated_hours) : null,
          tags: tagsArray.length > 0 ? tagsArray : null,
          is_recurring: false
        }),
      });

      if (!res.ok) throw new Error("Failed to create task");
      
      const newTask = await res.json();
      setTasks([newTask, ...tasks]);
      setFormData({
        title: "",
        description: "",
        due_date: "",
        category: "",
        priority: "medium",
        estimated_hours: "",
        tags: ""
      });
      setShowForm(false);
      fetchStats();
    } catch (error) {
      console.error("Error adding task:", error);
      setError("Failed to create task");
    }
  }

  async function toggleComplete(taskId) {
    try {
      const task = tasks.find(t => t.id === taskId);
      if (!task) return;

      const res = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({
          completed: !task.completed
        }),
      });

      if (!res.ok) throw new Error("Failed to update task");
      
      const updated = await res.json();
      setTasks(tasks.map(t => (t.id === updated.id ? updated : t)));
      fetchStats();
    } catch (error) {
      console.error("Error updating task:", error);
      setError("Failed to update task");
    }
  }

  async function deleteTask(taskId) {
    try {
      const res = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: "DELETE",
      });

      if (!res.ok) throw new Error("Failed to delete task");
      
      setTasks(tasks.filter(t => t.id !== taskId));
      fetchStats();
    } catch (error) {
      console.error("Error deleting task:", error);
      setError("Failed to delete task");
    }
  }

  async function updateTask(taskId, updates) {
    try {
      if (updates.priority) {
        updates.priority = updates.priority.toLowerCase();
      }
      
      const res = await fetch(`${API_URL}/tasks/${taskId}`, {
        method: "PUT",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify(updates),
      });

      if (!res.ok) throw new Error("Failed to update task");
      
      const updated = await res.json();
      setTasks(tasks.map(t => (t.id === updated.id ? updated : t)));
      fetchStats();
    } catch (error) {
      console.error("Error updating task:", error);
      setError("Failed to update task");
    }
  }

  const today = new Date();
today.setHours(0, 0, 0, 0);

const getFilteredTasks = () => {
  let filtered = [...tasks];

  // Filter by view
  switch (view) {
    case "today":
      filtered = filtered.filter(task => {
        if (task.completed) return false;
        if (!task.due_date) return false;
        const taskDate = new Date(task.due_date);
        taskDate.setHours(0, 0, 0, 0);
        return taskDate.getTime() === today.getTime();
      });
      break;

    case "upcoming":
      filtered = filtered.filter(task => {
        if (task.completed) return false;
        if (!task.due_date) return false;
        const taskDate = new Date(task.due_date);
        taskDate.setHours(0, 0, 0, 0);
        const tomorrow = new Date(today);
        tomorrow.setDate(tomorrow.getDate() + 1);
        const sevenDaysFromNow = new Date(today);
        sevenDaysFromNow.setDate(sevenDaysFromNow.getDate() + 7);
        return taskDate >= tomorrow && taskDate <= sevenDaysFromNow;
      });
      break;

    case "overdue":
      filtered = filtered.filter(task => {
        if (task.completed) return false;
        if (!task.due_date) return false;
        const taskDate = new Date(task.due_date);
        taskDate.setHours(0, 0, 0, 0);
        return taskDate < today;
      });
      break;

    case "pending":
      filtered = filtered.filter(task => !task.completed);
      break;

    case "completed":
      filtered = filtered.filter(task => task.completed);
      break;

    case "agenda":
      filtered = filtered.filter(task => {
        if (!task.due_date) return false;
        const taskDate = new Date(task.due_date);
        const selectedDate = new Date(agendaDate);
        taskDate.setHours(0, 0, 0, 0);
        selectedDate.setHours(0, 0, 0, 0);
        return taskDate.getTime() === selectedDate.getTime();
      });
      break;

    default:
      break;
  }

  // Apply category filter
  if (categoryFilter !== "All") {
    filtered = filtered.filter(task => task.category === categoryFilter);
  }

  // Apply priority filter
  if (priorityFilter !== "All") {
    filtered = filtered.filter(task => task.priority === priorityFilter);
  }

  return filtered;
};

const displayedTasks = getFilteredTasks();

const priorityColors = {
  low: "#6c757d",
  medium: "#ffc107",
  high: "#fd7e14",
  critical: "#dc3545",
};

return (
  <div className="app-container">
    <header className="app-header">
      <h1>📝 My Tasks</h1>
      <p className="subtitle">Stay organized and productive</p>
    </header>

    {error && (
      <div className="error-message">
        ⚠️ {error}
        <button onClick={() => setError("")} className="close-btn">×</button>
      </div>
    )}

    {/* STATS CARDS */}
    {stats && (
      <div className="stats-section">
        <div className="stat-card">
          <div className="stat-number">{stats.total_tasks}</div>
          <div className="stat-label">Total Tasks</div>
        </div>
        <div className="stat-card completed">
          <div className="stat-number">{stats.completed_tasks}</div>
          <div className="stat-label">Completed</div>
        </div>
        <div className="stat-card pending">
          <div className="stat-number">{stats.pending_tasks}</div>
          <div className="stat-label">Pending</div>
        </div>
        <div className="stat-card">
          <div className="stat-number">{stats.completion_rate.toFixed(0)}%</div>
          <div className="stat-label">Completion Rate</div>
        </div>
      </div>
    )}

    {/* NAVIGATION TABS */}
    <div className="nav-tabs">
      <button
        className={`tab ${view === "today" ? "active" : ""}`}
        onClick={() => setView("today")}
      >
        📅 Today
      </button>
      <button
        className={`tab ${view === "upcoming" ? "active" : ""}`}
        onClick={() => setView("upcoming")}
      >
        📆 Upcoming
      </button>
      <button
        className={`tab ${view === "overdue" ? "active" : ""}`}
        onClick={() => setView("overdue")}
      >
        ⚠️ Overdue
      </button>
      <button
        className={`tab ${view === "pending" ? "active" : ""}`}
        onClick={() => setView("pending")}
      >
        📋 All Tasks
      </button>
      <button
        className={`tab ${view === "completed" ? "active" : ""}`}
        onClick={() => setView("completed")}
      >
        ✅ Completed
      </button>
      <button
        className={`tab ${view === "agenda" ? "active" : ""}`}
        onClick={() => setView("agenda")}
      >
        🗓️ Agenda
      </button>
    </div>

    {/* ADD TASK BUTTON */}
    {!showForm && (
      <button className="btn-add-task" onClick={() => setShowForm(true)}>
        + Add New Task
      </button>
    )}

    {/* ADD TASK FORM */}
    {showForm && (
      <form className="task-form" onSubmit={addTask}>
        <div className="form-group">
          <input
            type="text"
            placeholder="What needs to be done?"
            value={formData.title}
            onChange={(e) => setFormData({ ...formData, title: e.target.value })}
            required
            className="form-input main"
          />
        </div>

        <div className="form-row">
          <input
            type="text"
            placeholder="Description (optional)"
            value={formData.description}
            onChange={(e) => setFormData({ ...formData, description: e.target.value })}
            className="form-input"
          />
          <input
            type="date"
            value={formData.due_date}
            onChange={(e) => setFormData({ ...formData, due_date: e.target.value })}
            className="form-input"
          />
        </div>

        <div className="form-row">
          <input
            type="text"
            placeholder="Category"
            value={formData.category}
            onChange={(e) => setFormData({ ...formData, category: e.target.value })}
            className="form-input"
          />
          <select
            value={formData.priority}
            onChange={(e) => setFormData({ ...formData, priority: e.target.value })}
            className="form-input"
          >
            <option value="low">Low Priority</option>
            <option value="medium">Medium Priority</option>
            <option value="high">High Priority</option>
            <option value="critical">Critical</option>
          </select>
        </div>

        <div className="form-row">
          <input
            type="number"
            placeholder="Estimated hours (optional)"
            step="0.5"
            min="0"
            value={formData.estimated_hours}
            onChange={(e) => setFormData({ ...formData, estimated_hours: e.target.value })}
            className="form-input"
          />
          <input
            type="text"
            placeholder="Tags (comma-separated)"
            value={formData.tags}
            onChange={(e) => setFormData({ ...formData, tags: e.target.value })}
            className="form-input"
          />
        </div>

        <div className="form-actions">
          <button type="submit" className="btn-primary">Create Task</button>
          <button
            type="button"
            className="btn-cancel"
            onClick={() => setShowForm(false)}
          >
            Cancel
          </button>
        </div>
      </form>
    )}

    {/* FILTERS */}
    <div className="filters">
      <select
        value={categoryFilter}
        onChange={(e) => setCategoryFilter(e.target.value)}
        className="filter-select"
      >
        <option value="All">All Categories</option>
        {categories.map((cat) => (
          <option key={cat} value={cat}>{cat}</option>
        ))}
      </select>

      <select
        value={priorityFilter}
        onChange={(e) => setPriorityFilter(e.target.value)}
        className="filter-select"
      >
        <option value="All">All Priorities</option>
        <option value="critical">Critical</option>
        <option value="high">High</option>
        <option value="medium">Medium</option>
        <option value="low">Low</option>
      </select>

      {view === "agenda" && (
        <input
          type="date"
          value={agendaDate}
          onChange={(e) => setAgendaDate(e.target.value)}
          className="filter-select"
        />
      )}
    </div>

    {/* TASKS LIST */}
    <div className="tasks-container">
      {loading && <div className="loading">Loading tasks...</div>}
      
      {!loading && displayedTasks.length === 0 ? (
        <div className="empty-state">
          {view === "completed" && "No completed tasks yet!"}
          {view === "today" && "No tasks for today. Enjoy your day! 🎉"}
          {view === "upcoming" && "No upcoming tasks. You're all caught up! ✨"}
          {view === "overdue" && "No overdue tasks. Great job! 👏"}
          {view !== "completed" && view !== "today" && view !== "upcoming" && view !== "overdue" && "No tasks to show."}
        </div>
      ) : (
        <div className="tasks-list">
          {displayedTasks.map((task) => (
            <TodoItem
              key={task.id}
              task={task}
              onToggle={toggleComplete}
              onDelete={deleteTask}
              onUpdate={updateTask}
              priorityColors={priorityColors}
            />
          ))}
        </div>
      )}
    </div>
  </div>
);
}

export default App;
