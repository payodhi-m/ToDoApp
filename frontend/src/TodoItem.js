import React, {useState} from "react";
import './TodoItem.css'

function TodoItem({todo, toggleComplete, deleteTodo, updateTodo}){
    const [isEditing, setIsEditing] = useState(false);
    const [title, setTitle] = useState(todo.title);

    const handleEdit = () => setIsEditing(true);
    const handleChange = (e) => setTitle(e.target.value);
    const handleBlur = () => {
        setIsEditing(false);
        updateTodo(todo.id, {title, completed: todo.completed});
    };

    const isOverdue = todo.due_date && new Date(todo.due_date) < new Date() && !todo.completed;

    return (
        <div className={`todo-item ${todo.completed ? "completed" : ""} ${
            isOverdue ? "overdue" : ""
        }`}>
        {/* <li> */}
            
            <input
                type="checkbox"
                checked={todo.completed}
                onChange={() => toggleComplete(todo)}
                className="checkbox" />

            {isEditing ? (
                <input
                    className="title"
                    value = {title}
                    onChange={handleChange}
                    onBlur={handleBlur}
                    autoFocus />
            ): (
                <span onClick={handleEdit}>{todo.title}</span>
            )}

            <span
                style={{
                color: isOverdue ? "red" : "gray",
                marginLeft: "1rem",
                fontWeight: isOverdue ? "bold" : "normal",
            }}>{todo.due_date ? `Due: ${todo.due_date}` : ""}
            </span>
            {todo.category && (
                <span style={{marginLeft: "0.5rem", fontStyle: "italic", color: "#555"}}>[{todo.category}]</span>
            )}
            <div className="actions">
            <button onClick={() => deleteTodo(todo.id)}>Delete</button>
            </div>
        {/* </li> */}
        </div>
        
    );
}

export default TodoItem;