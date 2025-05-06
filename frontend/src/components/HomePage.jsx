import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";

// Пример данных для постов
const mockPosts = [
  {
    id: 1,
    title: "Первый пост о филателии",
    content: "Сегодня мы начинаем обсуждение коллекции редких марок.",
    createdAt: "2025-05-01",
    author: "Петр Иванов",
  },
  {
    id: 2,
    title: "Встреча клуба",
    content: "Приглашаем всех на следующую встречу клуба по филателии.",
    createdAt: "2025-04-25",
    author: "Иван Петров",
  },
  {
    id: 3,
    title: "История марок",
    content: "Обсуждаем важнейшие исторические события через коллекции марок.",
    createdAt: "2025-04-15",
    author: "Анна Смирнова",
  },
];

const HomePage = () => {
  const [posts, setPosts] = useState(mockPosts);

  useEffect(() => {
    // Здесь можно будет интегрировать реальные данные с бэкенда
    // Например, вызвать API для получения последних постов
    // setPosts(полученные данные);
  }, []);

  return (
    <div className="container mx-auto p-6">
      <h2 className="text-4xl font-semibold mb-6">Добро пожаловать в Клуб Филателистов!</h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {posts.map((post) => (
          <div key={post.id} className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl">
            <h3 className="text-2xl font-semibold">{post.title}</h3>
            <p className="text-gray-600 mt-2">{post.content}</p>
            <p className="text-sm text-gray-400 mt-4">
              Автор: {post.author} | {new Date(post.createdAt).toLocaleDateString()}
            </p>
            <Link
              to={`/post/${post.id}`}
              className="mt-4 inline-block text-blue-600 hover:underline"
            >
              Читать дальше &rarr;
            </Link>
          </div>
        ))}
      </div>
    </div>
  );
};

export default HomePage;
