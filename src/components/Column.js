import React from "react";
import Task from "./Task";

const Column = ({ status, tasks, onDragOver, onDrop }) => {
  return (
    <div
      className="column pixel-corners"
      data-status={status}
      onDragOver={onDragOver}
      onDrop={onDrop}
    >
      <h2>{status}</h2>
      {tasks.map((task) => (
        <Task key={task.id} task={task} />
      ))}
    </div>
  );
};

export default Column;
