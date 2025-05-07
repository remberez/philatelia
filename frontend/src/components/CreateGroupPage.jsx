import React, { useState } from "react";
import groupService from "../services/groupService";

export default function CreateGroupPage() {
  const [name, setName] = useState("");
  const [description, setDescription] = useState("");
  const [groupname, setGroupname] = useState("");

  const handleSubmit = async (e) => {
    e.preventDefault();

    const newGroup = {
      name,
      description,
      groupname,
    };

    console.log("Создание группы:", newGroup);

    await groupService.createGroup(newGroup)

    setName("");
    setDescription("");
    setGroupname("");
  };

  return (
    <div className="max-w-2xl mx-auto p-6">
      <form
        onSubmit={handleSubmit}
        className="bg-white rounded-2xl shadow p-6 space-y-4"
      >
        <h2 className="text-2xl font-semibold mb-4">Создание новой группы</h2>

        <div>
          <label className="block text-sm font-medium mb-1">Название</label>
          <input
            type="text"
            value={name}
            onChange={(e) => setName(e.target.value)}
            className="w-full border rounded-lg px-4 py-2"
            placeholder="Например: Клуб любителей не ходить на пары"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">Описание</label>
          <textarea
            value={description}
            onChange={(e) => setDescription(e.target.value)}
            className="w-full border rounded-lg px-4 py-2"
            rows={4}
            placeholder="Кратко опишите, о чём ваша группа"
            required
          />
        </div>

        <div>
          <label className="block text-sm font-medium mb-1">
            Уникальное имя группы (groupname)
          </label>
          <input
            type="text"
            value={groupname}
            onChange={(e) => setGroupname(e.target.value)}
            className="w-full border rounded-lg px-4 py-2"
            placeholder="Например: ne_hodit_na_pari342"
            required
          />
        </div>

        <button
          type="submit"
          className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition"
        >
          Создать группу
        </button>
      </form>
    </div>
  );
}
