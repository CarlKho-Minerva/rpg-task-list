import React, { useState, useEffect, useCallback } from "react";
import { BrowserRouter as Router, Route, Link, Routes } from "react-router-dom";
import KanbanBoard from "./components/KanbanBoard";
import AddTaskForm from "./components/AddTaskForm";
import ErrorBoundary from "./components/ErrorBoundary";
import "./App.css";

const API_URL = process.env.REACT_APP_BASE_API_URL || "http://127.0.0.1:5000";

function App() {
  const [tasks, setTasks] = useState([]);
  const [isLoading, setIsLoading] = useState(true);
  const [error, setError] = useState(null);

  const fetchTasks = useCallback(async () => {
    setIsLoading(true);
    setError(null);
    try {
      const response = await fetch(`${API_URL}/api/tasks`);
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setTasks(data);
    } catch (error) {
      setError("Failed to fetch tasks. Please try again later.");
      console.error("Error fetching tasks:", error);
    } finally {
      setIsLoading(false);
    }
  }, []);

  useEffect(() => {
    fetchTasks();
  }, [fetchTasks]);

  const addTask = async (newTask) => {
    try {
      const response = await fetch(`${API_URL}/api/tasks`, {
        method: "POST",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify(newTask),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const data = await response.json();
      setTasks((prevTasks) => [...prevTasks, data]);
    } catch (error) {
      setError("Failed to add task. Please try again.");
      console.error("Error adding task:", error);
    }
  };

  const updateTaskStatus = async (taskId, newStatus) => {
    try {
      const response = await fetch(`${API_URL}/api/tasks/${taskId}`, {
        method: "PUT",
        headers: {
          "Content-Type": "application/json",
        },
        body: JSON.stringify({ status: newStatus }),
      });
      if (!response.ok) {
        throw new Error(`HTTP error! status: ${response.status}`);
      }
      const updatedTask = await response.json();
      setTasks((prevTasks) =>
        prevTasks.map((task) => (task.id === taskId ? updatedTask : task))
      );
    } catch (error) {
      setError("Failed to update task. Please try again.");
      console.error("Error updating task:", error);
    }
  };

  if (isLoading) {
    return <div>Loading...</div>;
  }

  if (error) {
    return <div>Error: {error}</div>;
  }

  return (
    <Router>
      <ErrorBoundary>
        <div className="background">
          <div className="flame"></div>
          <div className="container">
            <header>
              <h1 className="board-title">Epic Quest Board</h1>
              <nav>
                <Link to="/" className="nav-button pixel-corners">
                  Home
                </Link>
                <Link to="/add-task" className="nav-button pixel-corners">
                  Add New Quest
                </Link>
              </nav>
            </header>
            <Routes>
              <Route
                path="/"
                element={
                  <KanbanBoard
                    tasks={tasks}
                    updateTaskStatus={updateTaskStatus}
                  />
                }
              />
              <Route
                path="/add-task"
                element={<AddTaskForm addTask={addTask} />}
              />
            </Routes>
          </div>
        </div>
      </ErrorBoundary>
    </Router>
  );
}

export default App;
