import { api } from "./api";

class PostService {
    async getAllPosts() {
        return (await api.get("/posts")).data;
    }

    async groupPosts(id) {
        return (await api.get(`/groups/${id}/posts`)).data;
    }

    async createPost({group_id, title, text}) {
        return (await api.post("/posts/", {group_id, text, title})).data;
    }
}

export default new PostService();