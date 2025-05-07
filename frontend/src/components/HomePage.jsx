import React, { useState, useEffect } from "react";
import { Link } from "react-router-dom";
import postsService from "../services/postsService";

const HomePage = () => {
  const [posts, setPosts] = useState([]);

  useEffect(() => {
    async function fetchData() {
        setPosts(await postsService.getAllPosts());
    }

    fetchData();
}, []);

  return (
    <div className="container mx-auto py-6">
      <h2 className="text-4xl font-semibold mb-6">Статьи</h2>
      
      <div className="grid grid-cols-1 sm:grid-cols-2 md:grid-cols-3 gap-6">
        {posts.map((post) => (
          <div key={post.id} className="bg-white p-6 rounded-lg shadow-md hover:shadow-xl">
            <h3 className="text-2xl font-semibold">{post.title}</h3>
            <p className="text-gray-600 mt-2">{post.text}</p>
            <p className="text-sm text-gray-400 mt-4">
              Автор: {post.author} | {new Date(post.created_at).toLocaleDateString()}
            </p>
            <Link
              to={`/group/${post.group_id}`}
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
