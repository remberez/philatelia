import React, { useEffect, useState } from "react";
import groupService from "../services/groupService";
import postsService from "../services/postsService";

export default function CreatePostForm({ onSubmit }) {
  const [title, setTitle] = useState("");
  const [text, setText] = useState("");
  const [groups, setGroups] = useState([]);
  const [groupId, setGroupId] = useState(null);

  const [photoUrls, setPhotoUrls] = useState([""]); // массив ссылок

  const handlePhotoChange = (index, value) => {
    const newPhotos = [...photoUrls];
    newPhotos[index] = value;
    setPhotoUrls(newPhotos);
  };

  const addPhotoField = () => {
    setPhotoUrls([...photoUrls, ""]);
  };

  const removePhotoField = (index) => {
    const newPhotos = [...photoUrls];
    newPhotos.splice(index, 1);
    setPhotoUrls(newPhotos);
  };

  const handleSubmit = async (e) => {
    e.preventDefault();
    if (!title.trim() || !text.trim() || !groupId) return;

    const newPost = {
      title,
      text,
      group_id: groupId,
    };

    if (onSubmit) onSubmit(newPost);

    const postData = await postsService.createPost(newPost);

    // Загружаем изображения
    const validUrls = photoUrls.filter((url) => url.trim() !== "");
    for (const url of validUrls) {
      await postsService.addImage({
        photo_url: url,
        post_id: postData.id,
        group_id: groupId,
      });
    }

    // Очистить форму
    setTitle("");
    setText("");
    setPhotoUrls([""]);
  };

  useEffect(() => {
    async function fetchData() {
      const groupData = await groupService.getMyGroups();
      setGroups(groupData);
      if (groupData.length > 0) {
        setGroupId(groupData[0].id);
      }
    }

    fetchData();
  }, []);

  return (
    <form
      onSubmit={handleSubmit}
      className="bg-white rounded-2xl shadow p-6 space-y-4"
    >
      <h2 className="text-2xl font-semibold mb-4">Создать пост</h2>

      <div>
        <label className="block text-sm font-medium mb-1">Группа</label>
        <select
          value={groupId ?? ""}
          onChange={(e) => setGroupId(parseInt(e.target.value))}
          className="w-full border rounded-lg px-4 py-2"
          required
        >
          <option value="" disabled>
            Выберите группу
          </option>
          {groups.map((group) => (
            <option key={group.id} value={group.id}>
              {group.name}
            </option>
          ))}
        </select>
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Заголовок</label>
        <input
          type="text"
          value={title}
          onChange={(e) => setTitle(e.target.value)}
          className="w-full border rounded-lg px-4 py-2"
          placeholder="Введите заголовок"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Текст</label>
        <textarea
          value={text}
          onChange={(e) => setText(e.target.value)}
          className="w-full border rounded-lg px-4 py-2"
          rows={4}
          placeholder="Введите текст поста"
          required
        />
      </div>

      <div>
        <label className="block text-sm font-medium mb-1">Изображения (URL)</label>
        {photoUrls.map((url, index) => (
          <div key={index} className="flex items-center gap-2 mb-2">
            <input
              type="url"
              value={url}
              onChange={(e) => handlePhotoChange(index, e.target.value)}
              className="flex-grow border rounded-lg px-4 py-2"
              placeholder="https://example.com/image.jpg"
            />
            {photoUrls.length > 1 && (
              <button
                type="button"
                onClick={() => removePhotoField(index)}
                className="text-red-500 hover:underline text-sm"
              >
                Удалить
              </button>
            )}
          </div>
        ))}
        <button
          type="button"
          onClick={addPhotoField}
          className="text-blue-600 hover:underline text-sm mt-1"
        >
          + Добавить ещё изображение
        </button>
      </div>

      <button
        type="submit"
        className="bg-blue-600 text-white px-6 py-2 rounded-xl hover:bg-blue-700 transition"
      >
        Опубликовать
      </button>
    </form>
  );
}
