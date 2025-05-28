import React, { useEffect, useState } from "react";
import { useParams } from "react-router-dom";
import groupService from "../services/groupService";
import postsService from "../services/postsService";
import commentService from "../services/commentService";
import userStore from "../stores/userStore";

export default function GroupPage() {
  const { groupId } = useParams();

  const [group, setGroup] = useState({});
  const [posts, setPosts] = useState([]);
  const [members, setMembers] = useState([]);
  const [isMember, setIsMember] = useState(false);
  const [loading, setLoading] = useState(true);
  const [comments, setComments] = useState({}); // { [postId]: [comments] }
  const [commentInputs, setCommentInputs] = useState({}); // { [postId]: "" }
  const [editingComment, setEditingComment] = useState({}); // { [commentId]: text }

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

      // fetch comments for all posts
      const commentsObj = {};
      for (const post of postsData) {
        commentsObj[post.id] = await commentService.getComments(post.id);
      }
      setComments(commentsObj);

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

  const handleCommentInput = (postId, value) => {
    setCommentInputs((prev) => ({ ...prev, [postId]: value }));
  };

  const handleAddComment = async (postId) => {
    const text = commentInputs[postId]?.trim();
    if (!text) return;
    const newComment = await commentService.createComment(postId, text);
    setComments((prev) => ({
      ...prev,
      [postId]: [...(prev[postId] || []), newComment],
    }));
    setCommentInputs((prev) => ({ ...prev, [postId]: "" }));
  };

  const handleDeleteComment = async (postId, commentId) => {
    await commentService.deleteComment(commentId);
    setComments((prev) => ({
      ...prev,
      [postId]: prev[postId].filter((c) => c.id !== commentId),
    }));
  };

  const handleEditComment = (commentId, text) => {
    setEditingComment((prev) => ({ ...prev, [commentId]: text }));
  };

  const handleUpdateComment = async (postId, commentId) => {
    const text = editingComment[commentId]?.trim();
    if (!text) return;
    const updated = await commentService.updateComment(commentId, text);
    setComments((prev) => ({
      ...prev,
      [postId]: prev[postId].map((c) => (c.id === commentId ? updated : c)),
    }));
    setEditingComment((prev) => {
      const copy = { ...prev };
      delete copy[commentId];
      return copy;
    });
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
                {/* Комментарии */}
                <div className="mt-4">
                  <h4 className="font-semibold mb-2">Комментарии</h4>
                  <div className="space-y-2">
                    {(comments[post.id] || []).map((comment) => (
                      <div key={comment.id} className="flex items-start gap-2 group">
                        <div className="flex-1">
                          <span className="font-medium">{comment.user_id === userStore.user?.id ? "Вы" : `Пользователь #${comment.user_id}`}</span>
                          <span className="ml-2 text-xs text-gray-500">{new Date(comment.created_at).toLocaleString("ru-RU")}</span>
                          {editingComment[comment.id] !== undefined ? (
                            <div className="flex gap-2 mt-1">
                              <input
                                className="border rounded px-2 py-1 text-sm flex-1"
                                value={editingComment[comment.id]}
                                onChange={e => handleEditComment(comment.id, e.target.value)}
                              />
                              <button className="text-blue-600 text-xs" onClick={() => handleUpdateComment(post.id, comment.id)}>Сохранить</button>
                              <button className="text-gray-500 text-xs" onClick={() => handleEditComment(comment.id, undefined)}>Отмена</button>
                            </div>
                          ) : (
                            <div className="mt-1 text-sm">{comment.text}</div>
                          )}
                        </div>
                        {comment.user_id === userStore.user?.id && editingComment[comment.id] === undefined && (
                          <div className="flex flex-col gap-1 opacity-0 group-hover:opacity-100 transition">
                            <button className="text-xs text-blue-600" onClick={() => handleEditComment(comment.id, comment.text)}>Изменить</button>
                            <button className="text-xs text-red-500" onClick={() => handleDeleteComment(post.id, comment.id)}>Удалить</button>
                          </div>
                        )}
                      </div>
                    ))}
                  </div>
                  {userStore.isAuth && (
                    <div className="flex gap-2 mt-2">
                      <input
                        className="border rounded px-2 py-1 flex-1"
                        placeholder="Написать комментарий..."
                        value={commentInputs[post.id] || ""}
                        onChange={e => handleCommentInput(post.id, e.target.value)}
                        onKeyDown={e => { if (e.key === "Enter") handleAddComment(post.id); }}
                      />
                      <button
                        className="bg-blue-600 text-white px-4 py-1 rounded"
                        onClick={() => handleAddComment(post.id)}
                      >
                        Отправить
                      </button>
                    </div>
                  )}
                </div>
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
