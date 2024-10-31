# Kanban Board

This project is a Kanban board application built with React and Flask. The frontend is developed using React, while the backend is powered by Flask. The application allows users to manage tasks by adding, updating, and deleting them.

## Project Structure

```
kanban-board/
├── public/
│   ├── index.html
│   └── ...
├── src/
│   ├── components/
│   │   ├── AddTaskForm.js
│   │   ├── Column.js
│   │   ├── KanbanBoard.js
│   │   └── ...
│   ├── App.js
│   ├── index.js
│   └── ...
├── package.json
├── package-lock.json
└──

README.md


```

## Getting Started

### Prerequisites

- Node.js and npm installed on your machine.
- Python and Flask installed on your machine.

### Installation

1. **Clone the repository**:

   ```sh
   git clone <repository-url>
   cd kanban-board
   ```

2. **Install frontend dependencies**:

   ```sh
   npm install
   ```

3. **Install backend dependencies**:

   Navigate to the `kanban` folder and install the required Python packages:

   ```sh
   cd ../kanban
   pip install -r requirements.txt
   ```

### Running the Application

1. **Start the Flask backend**:

   ```sh
   python app.py
   ```

   The Flask server will start on `http://127.0.0.1:5000`.

2. **Start the React frontend**:

   ```sh
   npm start
   ```

   The React application will start on `http://localhost:3000`.

### API Endpoints

- **GET /api/tasks**: Retrieve all tasks.
- **POST /api/tasks**: Add a new task.
- **DELETE /api/tasks/<task_id>**: Remove a task by ID.
- **PUT /api/tasks/<task_id>**: Update the status of a task by ID.

### Components

- **App.js**: The main component that sets up routing and renders the Kanban board and Add Task form.
- **KanbanBoard.js**: The component that displays the tasks in columns based on their status.
- **AddTaskForm.js**: The component that provides a form to add new tasks.
- **Column.js**: The component that represents a column in the Kanban board.

### Styling

The application uses CSS for styling. The styles are defined in the `src` folder.

### Contributing

Contributions are welcome! Please open an issue or submit a pull request for any improvements or bug fixes.

### License

This project is licensed under the MIT License.
