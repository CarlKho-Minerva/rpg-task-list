import React from "react";

const Task = ({ task }) => {
  const onDragStart = (e) => {
    e.dataTransfer.setData("text", task.id);
  };

  return (
    <div
      className="task pixel-corners"
      draggable="true"
      onDragStart={onDragStart}
    >
      {task.description}
    </div>
  );
};

export default Task;
