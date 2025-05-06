import { api } from "./api";

class PostService {
    async getAllPosts() {
        return await api.get("/posts");
    }
}

export default new PostService();