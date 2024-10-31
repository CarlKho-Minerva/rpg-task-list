import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

const AddTaskForm = ({ addTask }) => {
  const [description, setDescription] = useState("");
  const [status, setStatus] = useState("Prophecies");
  const navigate = useNavigate();

  const handleSubmit = async (e) => {
    e.preventDefault();
    await addTask({ description, status });
    setDescription("");
    setStatus("Prophecies");
    navigate("/");
  };

  return (
    <form className="add-task pixel-corners" onSubmit={handleSubmit}>
      <input
        type="text"
        value={description}
        onChange={(e) => setDescription(e.target.value)}
        placeholder="Scribe thy new quest here..."
        required
      />
      <select value={status} onChange={(e) => setStatus(e.target.value)}>
        <option value="Prophecies">Prophecies</option>
        <option value="Quests Begun">Quests Begun</option>
        <option value="Trial by Combat">Trial by Combat</option>
        <option value="Enchantments">Enchantments</option>
        <option value="Legends">Legends</option>
      </select>
      <button type="submit" className="pixel-corners">
        Embark on Quest
      </button>
    </form>
  );
};

export default AddTaskForm;
