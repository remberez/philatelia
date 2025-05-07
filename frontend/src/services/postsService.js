import { api } from "./api";

class PostService {
    async getAllPosts() {
        return (await api.get("/posts")).data;
    }

    async groupPosts(id) {
        return (await api.get(`/groups/${id}/posts`)).data;
    }
}

export default new PostService();