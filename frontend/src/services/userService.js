import userStore from '../stores/userStore';
import { api } from './api';

const userService = {
  async register(username, email, password) {
    try {
      const response = await api.post('/auth/register', {
        username,
        email,
        password,
      });
      return response.data;
    } catch (error) {
      console.error("Registration error:", error);
      throw new Error("Registration failed");
    }
  },

  async login(email, password) {
    try {
      const formData = new FormData();
      formData.append('grant_type', 'password');
      formData.append('username', email); 
      formData.append('password', password);
    
      const response = await api.post('/auth/token', formData, {
        headers: {
          'Content-Type': 'application/x-www-form-urlencoded', // Правильный тип контента
        },
      });  // Отправляем данные
  
      const { access_token } = response.data;
  
      if (access_token) {
        localStorage.setItem('token', access_token);
        userStore.setUser(userService.getUser());
        return access_token;
      }
  
      throw new Error("Authorization failed");
    } catch (error) {
      console.error("Login error:", error);
      throw new Error("Login failed");
    }
  },

  logout() {
    localStorage.removeItem("token");
  },

  async getUser() {
    try {
      const response = await api.get("/auth/me");
      return response.data;
    } catch (error) {
      console.error("Error fetching user data:", error);
      throw new Error("Failed to fetch user data");
    }
  },

  async updateMe(data) {
    const resposne = await api.put("/auth/me", data);
    return resposne.data;
  }
};

export default userService;
