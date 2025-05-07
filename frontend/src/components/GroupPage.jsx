import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import groupService from "../services/groupService";
import postsService from "../services/postsService";

export default function GroupPage() {
  const { groupId } = useParams();

  const [group, setGroup] = useState({});
  const [posts, setPosts] = useState([]);
  const [members, setMembers] = useState([]);
  const [isMember, setIsMember] = useState(false);
  const [loading, setLoading] = useState(true);

  useEffect(() => {
    async function fetchData() {
      const groupData = await groupService.getGroup(groupId);
      setGroup(groupData);

      const postsData = await postsService.groupPosts(groupId);
      setPosts(postsData);

      const membersData = await groupService.getMembers(groupId);
      setMembers(membersData);

      const membership = await groupService.isMember(groupId);
      setIsMember(membership);

      setLoading(false);
    }

    fetchData();
  }, [groupId]);

  const handleJoinLeave = async () => {
    if (isMember) {
      await groupService.leaveGroup(groupId);
    } else {
      await groupService.joinGroup(groupId);
    }
    const membersData = await groupService.getMembers(groupId);
    setMembers(membersData);
    const membership = await groupService.isMember(groupId);
    setIsMember(membership);
  };

  if (loading) return <div className="text-center mt-10">Загрузка...</div>;

  return (
    <div className="max-w-7xl mx-auto p-6">
      {/* Верхняя панель */}
      <div className="flex justify-between items-center bg-white rounded-2xl shadow p-6 mb-6">
        <div>
          <h1 className="text-3xl font-bold">{group.name}</h1>
          <p className="text-gray-600">@{group.groupname}</p>
          <p className="mt-2 text-gray-800">{group.description}</p>
        </div>
        <button
          onClick={handleJoinLeave}
          className={`px-6 py-2 rounded-xl font-medium shadow transition 
            ${
              isMember
                ? "bg-gray-200 text-gray-800 hover:bg-gray-300"
                : "bg-blue-600 text-white hover:bg-blue-700"
            }`}
        >
          {isMember ? "Выйти из группы" : "Вступить в группу"}
        </button>
      </div>

      {/* Содержимое */}
      <div className="grid grid-cols-1 md:grid-cols-3 gap-6">
        {/* Левая колонка — посты */}
        <div className="md:col-span-2 space-y-6">
          <section className="bg-white rounded-2xl shadow p-6">
            <h2 className="text-2xl font-semibold mb-4">Посты</h2>
            {posts.map((post) => (
              <div
                key={post.id}
                className="border-b pb-4 mb-4 last:border-none last:pb-0 last:mb-0"
              >
                <h3 className="text-xl font-bold">{post.title}</h3>
                <p className="text-gray-600 text-sm">
                  Автор: {post.author} ·{" "}
                  {new Date(post.created_at).toLocaleString("ru-RU")}
                </p>
                <p className="mt-2">{post.text}</p>
                {post.photos.length > 0 && (
                  <div className="mt-4 grid grid-cols-2 gap-4">
                    {post.photos.map((photo) => (
                      <img
                        key={photo.id}
                        src={photo.photo_url}
                        alt="Фото поста"
                        className="rounded-lg w-full h-40 object-cover"
                      />
                    ))}
                  </div>
                )}
              </div>
            ))}
            {posts.length === 0 && (
              <p className="text-gray-500">Постов пока нет.</p>
            )}
          </section>
        </div>

        {/* Правая колонка — участники */}
        <aside className="bg-white rounded-2xl shadow p-6 h-fit">
          <h2 className="text-2xl font-semibold mb-4">Участники ({members.length})</h2>
          <ul className="space-y-2">
            {members.map((member) => (
              <li key={member.id}>
                <div className="text-sm">
                  <span className="font-medium">{member.username}</span>
                  <div className="text-gray-500">{member.email}</div>
                </div>
              </li>
            ))}
          </ul>
        </aside>
      </div>
    </div>
  );
}
