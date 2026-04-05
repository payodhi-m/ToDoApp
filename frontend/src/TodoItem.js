import React, { useState } from "react";
import "./TodoItem.css";

function TodoItem({ task, onToggle, onDelete, onUpdate, priorityColors }) {
  const [isEditing, setIsEditing] = useState(false);
  const [editingTitle, setEditingTitle] = useState(task.title);
  const [editingDescription, setEditingDescription] = useState(task.description || "");
  const [editingPriority, setEditingPriority] = useState(task.priority);
  const [editingCategory, setEditingCategory] = useState(task.category || "");
  const [editingDueDate, setEditingDueDate] = useState(task.due_date || "");
  const [editingEstimatedHours, setEditingEstimatedHours] = useState(task.estimated_hours || "");

  const handleEdit = () => setIsEditing(true);

  const handleSave = () => {
    onUpdate(task.id, {
      title: editingTitle,
      description: editingDescription || null,
      priority: editingPriority,
      category: editingCategory || null,
      due_date: editingDueDate || null,
      estimated_hours: editingEstimatedHours ? parseFloat(editingEstimatedHours) : null,
    });
    setIsEditing(false);
  };

  const handleCancel = () => {
    setEditingTitle(task.title);
    setEditingDescription(task.description || "");
    setEditingPriority(task.priority);
    setEditingCategory(task.category || "");
    setEditingDueDate(task.due_date || "");
    setEditingEstimatedHours(task.estimated_hours || "");
    setIsEditing(false);
  };

  const isOverdue =
    task.due_date &&
    new Date(task.due_date) < new Date() &&
    !task.completed;

  const formatDate = (dateStr) => {
    if (!dateStr) return "";
    return new Date(dateStr).toLocaleDateString("en-US", {
      month: "short",
      day: "numeric",
      year: "numeric",
    });
  };

  return (
    <div
      className={`todo-item ${task.completed ? "completed" : ""} ${
        isOverdue ? "overdue" : ""
      }`}
      style={{
        borderLeft: `4px solid ${priorityColors[task.priority] || "#6c757d"}`,
      }}
    >
      {isEditing ? (
        <div className="edit-form">
          <input
            type="text"
            value={editingTitle}
            onChange={(e) => setEditingTitle(e.target.value)}
            placeholder="Task title"
            className="edit-input"
          />
          <textarea
            value={editingDescription}
            onChange={(e) => setEditingDescription(e.target.value)}
            placeholder="Description"
            className="edit-input"
            rows="3"
          />
          <div className="edit-row">
            <input
              type="text"
              value={editingCategory}
              onChange={(e) => setEditingCategory(e.target.value)}
              placeholder="Category"
              className="edit-input"
            />
            <input
              type="date"
              value={editingDueDate}
              onChange={(e) => setEditingDueDate(e.target.value)}
              className="edit-input"
            />
          </div>
          <div className="edit-row">
            <select
              value={editingPriority}
              onChange={(e) => setEditingPriority(e.target.value)}
              className="edit-input"
            >
              <option value="low">Low</option>
              <option value="medium">Medium</option>
              <option value="high">High</option>
              <option value="critical">Critical</option>
            </select>
            <input
              type="number"
              value={editingEstimatedHours}
              onChange={(e) => setEditingEstimatedHours(e.target.value)}
              placeholder="Estimated hours"
              step="0.5"
              min="0"
              className="edit-input"
            />
          </div>
          <div className="edit-actions">
            <button onClick={handleSave} className="btn-save">
              Save
            </button>
            <button onClick={handleCancel} className="btn-cancel">
              Cancel
            </button>
          </div>
        </div>
      ) : (
        <>
          <div className="task-checkbox">
            <input
              type="checkbox"
              checked={task.completed}
              onChange={() => onToggle(task.id)}
              className="checkbox-input"
            />
          </div>

          <div className="task-content">
            <div className="task-header">
              <span
                className="task-title"
                style={{
                  textDecoration: task.completed ? "line-through" : "none",
                  color: task.completed ? "#999" : "#333",
                }}
              >
                {task.title}
              </span>
              <div className="task-badges">
                <span
                  className="badge priority-badge"
                  style={{
                    background: priorityColors[task.priority] || "#6c757d",
                  }}
                >
                  {task.priority}
                </span>
                {task.completed && (
                  <span className="badge completed-badge">✓ Done</span>
                )}
                {isOverdue && !task.completed && (
                  <span className="badge overdue-badge">⚠️ Overdue</span>
                )}
              </div>
            </div>

            {task.description && (
              <p className="task-description">{task.description}</p>
            )}

            <div className="task-metadata">
              {task.category && (
                <span className="tag category-tag">📂 {task.category}</span>
              )}
              {task.due_date && (
                <span
                  className="tag due-date-tag"
                  style={{
                    color: isOverdue && !task.completed ? "white" : "#666",
                    background: isOverdue && !task.completed ? "#dc3545" : "#f0f0f0",
                  }}
                >
                  📅 {formatDate(task.due_date)}
                </span>
              )}
              {task.estimated_hours && (
                <span className="tag estimate-tag">
                  ⏱️ {task.estimated_hours}h
                </span>
              )}
              {task.time_spent_hours > 0 && (
                <span className="tag spent-tag">
                  ✓ {task.time_spent_hours}h spent
                </span>
              )}
              {task.tags && Array.isArray(task.tags) && task.tags.length > 0 && (
                <div className="tags-container">
                  {task.tags.map((tag, index) => (
                    <span key={index} className="tag">
                      #{tag}
                    </span>
                  ))}
                </div>
              )}
            </div>
          </div>

          <div className="task-actions">
            <button
              onClick={() => handleEdit()}
              className="btn-action btn-edit"
              title="Edit task"
            >
              ✎ Edit
            </button>

            <button
              onClick={() => onDelete(task.id)}
              className="btn-action btn-delete"
              title="Delete task"
            >
              🗑 Delete
            </button>
          </div>
        </>
      )}
    </div>
  );
}

export default TodoItem;
