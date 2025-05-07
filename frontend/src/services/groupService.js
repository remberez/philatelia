import { api } from "./api";

class GroupService {
    async getGroup(id) {
        const response = await api.get(`/groups/${id}`);
        return response.data;
    }

    async getMembers(id) {
        const reponse = await api.get(`/groups/${id}/members`);
        return reponse.data;
    }

    async isMember(groupId) {
        try {
            const response = await api.get(`/groups/${groupId}/is-member`);
            return response.data.is_member;
        } catch (e) {
            if (e.status === 401) {
                return false;
            }
        }
    }

    async joinGroup(groupId) {
        try {
            const response = await api.get(`/groups/${groupId}/join`);
            return response.data;
        } catch (error) {
            console.log("unauth")
        }
    }

    async leaveGroup(groupId) {
        try {
            const response = await api.delete(`/groups/${groupId}/leave`);
            return response.data;
        } catch (error) {
            console.log("unauth")
        }
    }

    async getMyGroups() {
        const resposne = await api.get("/groups/my");
        return resposne.data;
    }

    async createGroup({name, description, groupname}) {
        const response = await api.post("/groups", {name, description, groupname});
        return response.data;
    }
}

export default new GroupService();
