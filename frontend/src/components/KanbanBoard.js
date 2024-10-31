import React from "react";
import Column from "./Column";

const KanbanBoard = ({ tasks, updateTaskStatus }) => {
  const statuses = [
    "Prophecies",
    "Quests Begun",
    "Trial by Combat",
    "Enchantments",
    "Legends",
  ];

  const onDragOver = (e) => {
    e.preventDefault();
  };

  const onDrop = (e, status) => {
    const taskId = e.dataTransfer.getData("text");
    updateTaskStatus(taskId, status);
  };

  return (
    <div className="board">
      {statuses.map((status) => (
        <Column
          key={status}
          status={status}
          tasks={tasks.filter((task) => task.status === status)}
          onDragOver={onDragOver}
          onDrop={(e) => onDrop(e, status)}
        />
      ))}
    </div>
  );
};

export default KanbanBoard;
