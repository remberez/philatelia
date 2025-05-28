import {api} from "./api";

const commentService = {
  async getComments(postId) {
    const res = await api.get(`/comments/post/${postId}`);
    return res.data;
  },
  async createComment(postId, text) {
    const res = await api.post("/comments/", { post_id: postId, text });
    return res.data;
  },
  async updateComment(commentId, text) {
    const res = await api.patch(`/comments/${commentId}`, { text });
    return res.data;
  },
  async deleteComment(commentId) {
    await api.delete(`/comments/${commentId}`);
  },
};

export default commentService;
