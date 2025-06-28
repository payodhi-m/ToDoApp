import React, { useEffect, useState } from "react";
import TodoItem from "./TodoItem";
import './App.css';
import './TodoItem.css';

const API_URL = "http://127.0.0.1:8000"

function App(){
  const [todos, setTodos] = useState([]);
  const [newTitle, setNewTitle]  = useState("");
  // const [filter, setFilter] = useState("all"); //all | active | completed
  // const [searchQuery, setSearchQuery] = useState(""); //text search
  const [newDueDate, setNewDueDate] = useState("");
  const [newCategory, setNewCategory] = useState("");
  const [categoryFilter, setCategoryFilter] = useState("All");
  const [title, setTitle] = useState("");
  const [dueDate, setDueDate] = useState("");
  const [category, setCategory] = useState("");
  const [filter, setFilter] = useState("all");
  const [filterCategory, setFilterCategory] = useState("all");
  const [searchQuery, setSearchQuery] = useState("");

  useEffect(() => {
    fetchTodos();

  }, []);


  async function fetchTodos(){
    const res = await fetch(`${API_URL}/todos`);
    const data = await res.json();
    setTodos(data);

  }

  async function addTodo(){
    if(!newTitle.trim()) return;

    const newTodo = {id: 0, title: newTitle, completed: false, due_date: newDueDate || null, category: newCategory || null,};
    const res = await fetch(`${API_URL}/todos`, {
      method: "POST",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(newTodo),

    });

    const data = await res.json();
    setTodos([...todos, data]);
    setNewTitle("")
    setNewDueDate("");
    setNewCategory("");
  }

  async function toggleComplete(todo){
    const updatedTodo = {
      title: todo.title, 
      completed: !todo.completed,
      due_date: todo.due_date,
      category: todo.category,};
      
      const response = await fetch(`${API_URL}/todos/${todo.id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(updatedTodo),
    });

    if(!response.ok){
      console.error("Failed to update todo");
      return;
    }

    const updated = await response.json();

    //Refetching from back end instead of relying on local state
    setTodos(todos.map(t => (t.id === updated.id ? updated : t)));
    // setTodos(todos.map(t => t.id === todo.id ? { ...t, completed: !todo.completed }: t));
  }

  async function deleteTodo(todoId){
    await fetch(`${API_URL}/todos/${todoId}`, {method: "DELETE"});
    await fetchTodos();
    setTodos(todos.filter(t => t.id !== todoId));
  }

  async function updateTodo(id, updatedTodo){
    await fetch(`$(API_URL)/todos/${id}`, {
      method: "PUT",
      headers: {"Content-Type": "application/json"},
      body: JSON.stringify(updatedTodo),
    });

    setTodos((prevTodos) => prevTodos.map((t) => t.id === id ? { ...t, title: updatedTodo.title} : t));
  }

  const filterTodos = todos.filter((todo) => {
    if (filter === "active") return !todo.completed;
    if (filter === "completed") return todo.completed;
    return true;
  })
  .filter((todo) => {
    return todo.title.toLowerCase().includes(searchQuery.toLocaleLowerCase());
  })
  .filter((todo) => {
    if (categoryFilter === "All") return true;
    return todo.category === categoryFilter;
  });
  
  const totalTodos = todos.length;
  const completedTodos = todos.filter(todo => todo.completed).length;

  const progressPercent = totalTodos === 0 ? 0 : Math.round((completedTodos / totalTodos) * 100);

  let progressColor = "#dc3545";
  if (progressPercent >= 70){
    progressColor = "#28a745";

  }
  else if (progressPercent >=40){
    progressColor = "#ffc107";
  }

  const taskCompletedToday = todos.filter(todo => {
    if (!todo.completed_at) return false;
    const completedDate = new Date(todo.completed_at);
    const today = new Date();
    return (
      completedDate.getFullYear() === today.getFullYear() &&
      completedDate.getMonth() === today.getMonth() &&
      completedDate.getDate() === today.getDate()
    );
  }).length;

  return (
    <div className="app-container">
      <h1 className="header">To-Do List</h1>
      {/* <div className="filters">
        <button
          className={filter === "all" ? "active" : ""}
          onClick={() => setFilter("all")} > All 
        </button>

        <button 
          className={filter === "active" ? "active" : ""}
          onClick={() => setFilter("active")}> Active
        </button>

        <button 
          className={filter === "completed" ? "active" : ""}
          onClick={() => setFilter("completed")}> Completed
        </button>
      </div>

      <input
        type="text"
        placeholder="New To-Do"
        value={newTitle}
        onChange={(e) => setNewTitle(e.target.value)}
      />

      <input
        type="text"
        placeholder="Category"
        value={newCategory}
        onChange={(e) => setNewCategory(e.target.value)}
        style={{marginLeft: "0.5rem"}} />

      <input type="date"
        value={newDueDate}
        onChange={(e) => setNewDueDate(e.target.value)} />
      <button className="actions" onClick={addTodo}>Add</button>

      {/* <div style ={{ marginBottom: "1rem"}}>
          <button onClick={() => setFilter("all")}>All</button>
          <button onClick={() => setFilter("active")}>Active</button>
          <button onClick={() => setFilter("completed")}>Completed</button>

          <input
            className="search-input"
            type="text"
            placeholder="Search todos"
            value={searchQuery}
            onChange={(e) => setSearchQuery(e.target.value)}
            />
      </div> */}

      {/* Progress Bar */}
      {/* <div className="progress-bar-container"> 
          <div style={{fontWeight: "bold", marginBottom: "0.5rem"}}>Progress : {progressPercent}%</div>
          <div style={{ background: "#ddd", height: "12px", borderRadius: "8px", overflow: "hidden"}}>
            <div className="progress-bar" style={{
              width: `${progressPercent}%`,
              height: "100%",
              background: "#4caf50",
              transition: "width 0.3s ease-in-out"
            }}></div>
          </div>
          </div> */}

      {/* <select
        value={categoryFilter}
        onChange={(e) => setCategoryFilter(e.target.value)}
        style={{marginBottom: "1rem", marginLeft: "1rem"}}>
      <option value = "All">All Category</option>
      {[...new Set(todos.map(todo => todo.category).filter(Boolean))].map(cat => (<option key={cat} val={cat}>{cat}</option>))}
      </select>

      <div className="completed-today"> Task Completed today: {taskCompletedToday}
      </div> */}

      

<form
  className="todo-form"
  onSubmit={async (e) => {
    e.preventDefault();
    if (!title.trim()) return;

    const newTodo = {
      title,
      completed: false,
      due_date: dueDate || null,
      category,
    };

    const response = await fetch(`${API_URL}/todos`, {
      method: "POST",
      headers: { "Content-Type": "application/json" },
      body: JSON.stringify(newTodo),
    });

    const data = await response.json();
    setTodos([...todos, data]);

    // Reset input fields
    setTitle("");
    setDueDate("");
    setCategory("");
  }}
>
  <input
    type="text"
    placeholder="Enter task title"
    value={title}
    onChange={(e) => setTitle(e.target.value)}
  />

  <input
    type="date"
    value={dueDate}
    onChange={(e) => setDueDate(e.target.value)}
  />

  <input
    type="text"
    placeholder="Category (e.g., Work, Personal)"
    value={category}
    onChange={(e) => setCategory(e.target.value)}
  />

  <button type="submit"> Add Todo</button>
</form>

<div className="filters">
  <button
    className={filter === "all" ? "active" : ""}
    onClick={() => setFilter("all")}
  >
    All
  </button>
  <button
    className={filter === "active" ? "active" : ""}
    onClick={() => setFilter("active")}
  >
    Active
  </button>
  <button
    className={filter === "completed" ? "active" : ""}
    onClick={() => setFilter("completed")}
  >
    Completed
  </button>


  <select
    value={categoryFilter}
    onChange={(e) => setCategoryFilter(e.target.value)}
  >
    <option value="All">All Categories</option>
    {[...new Set(todos.map(todo => todo.category).filter(Boolean))].map(cat => (
      <option key={cat} value={cat}>{cat}</option>
    ))}
  </select>

  <input
    type="text"
    placeholder="Search by title..."
    value={searchQuery}
    onChange={(e) => setSearchQuery(e.target.value)}
  />
  {/* Progress Bar */}
  <div className="progress-label">Progress : {progressPercent}%</div>
       <div className="progress-bar-container"> 
          
            <div className="progress-bar" style={{
              width: `${progressPercent}%`,
              backgroundColor: progressColor
            }}></div>

        </div> 
  <ul>
        {filterTodos.map((todo) => (
          <TodoItem
            key={todo.id}
            todo={todo}
            toggleComplete={toggleComplete}
            deleteTodo={deleteTodo}
            updateTodo={updateTodo}/>
        ))} 
      </ul>
   

      <div className="completed-today"> Task Completed today: {taskCompletedToday}
      </div>
</div>
        {/* {todos.map((todo) => (
          <li key={todo.id} style={{ margin: "1rem 0" }}>
            <input
              type="checkbox"
              checked={todo.completed}
              onChange={() => toggleComplete(todo)}
              // disabled={todo.completed}
            />
            <span
              style={{
                textDecoration: todo.completed ? "line-through" : "none",
                marginLeft: "0.5rem",
              }}
            >
              {todo.title}
            </span>
            <button
              onClick={() => deleteTodo(todo.id)}
              style={{ marginLeft: "1rem" }}
            >
              Delete
            </button>
          </li>
        ))} */}
      {/* {/* </ul> */}
    </div> 
  );

}


// import logo from './logo.svg';
// import './App.css';

// function App() {
//   return (
//     <div className="App">
//       <header className="App-header">
//         <img src={logo} className="App-logo" alt="logo" />
//         <p>
//           Edit <code>src/App.js</code> and save to reload.
//         </p>
//         <a
//           className="App-link"
//           href="https://reactjs.org"
//           target="_blank"
//           rel="noopener noreferrer"
//         >
//           Learn React
//         </a>
//       </header>
//     </div>
//   );
// }

export default App;
