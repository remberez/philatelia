import React, { useState } from "react";
import userService from "../services/userService";

export default function RegisterPage() {
  const [formData, setFormData] = useState({
    username: "",
    email: "",
    password: "",
  });

  const handleChange = (e) => {
    setFormData((prev) => ({
      ...prev,
      [e.target.name]: e.target.value,
    }));
  };

  const handleSubmit = async (e) => {
    e.preventDefault();

    const userData = {
      username: formData.username,
      email: formData.email,
      password: formData.password,
    };

    console.log("Данные для регистрации:", userData);

    const data = await userService.register(userData.username, userData.email, userData.password);
    console.log(data);
  };

  return (
    <div className="max-w-md mx-auto mt-10 p-6 bg-white rounded-2xl shadow">
      <h1 className="text-3xl font-bold mb-6 text-center">Регистрация</h1>
      <form onSubmit={handleSubmit} className="space-y-4">
        <div>
          <label className="block mb-1 text-sm font-medium">Имя пользователя</label>
          <input
            type="text"
            name="username"
            value={formData.username}
            onChange={handleChange}
            className="w-full border px-4 py-2 rounded-lg"
            placeholder="Введите имя пользователя"
            required
          />
        </div>
        <div>
          <label className="block mb-1 text-sm font-medium">Email</label>
          <input
            type="email"
            name="email"
            value={formData.email}
            onChange={handleChange}
            className="w-full border px-4 py-2 rounded-lg"
            placeholder="Введите email"
            required
          />
        </div>
        <div>
          <label className="block mb-1 text-sm font-medium">Пароль</label>
          <input
            type="password"
            name="password"
            value={formData.password}
            onChange={handleChange}
            className="w-full border px-4 py-2 rounded-lg"
            placeholder="Введите пароль"
            required
          />
        </div>
        <button
          type="submit"
          className="w-full bg-blue-600 text-white py-2 rounded-xl hover:bg-blue-700 transition"
        >
          Зарегистрироваться
        </button>
      </form>
    </div>
  );
}
