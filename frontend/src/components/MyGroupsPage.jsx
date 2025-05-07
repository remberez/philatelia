import React, { useEffect, useState } from "react";
import groupService from "../services/groupService";
import { Link } from "react-router-dom";

export default function MyGroupsPage() {
  const [groups, setGroups] = useState([]);

  useEffect(() => {
    async function fetchGroups() {
      try {
        const myGroups = await groupService.getMyGroups();
        setGroups(myGroups);
      } catch (error) {
        console.error("Ошибка при загрузке групп:", error);
      }
    }

    fetchGroups();
  }, []);

  return (
    <div className="p-6">
      <h1 className="text-3xl font-bold mb-6">Мои группы</h1>

      {groups.length === 0 ? (
        <p className="text-gray-600">У вас пока нет групп.</p>
      ) : (
        <div className="grid grid-cols-1 sm:grid-cols-2 lg:grid-cols-3 gap-4">
          {groups.map((group) => (
            <div
              key={group.id}
              className="border rounded-2xl p-4 shadow bg-white flex flex-col justify-between"
            >
              <div>
                <h2 className="text-xl font-semibold">{group.name}</h2>
                <p className="text-sm text-gray-500 mb-4">{group.description}</p>
              </div>
              <Link
                to={`/create-post`}
                className="mt-auto text-sm text-blue-600 hover:underline"
              >
                ✏️ Создать пост
              </Link>
            </div>
          ))}
        </div>
      )}
    </div>
  );
}
