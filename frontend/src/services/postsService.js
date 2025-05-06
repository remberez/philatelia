import { api } from "./api";

class PostService {
    async getAllPosts() {
        return (await api.get("/posts")).data;
    }
}

export default new PostService();