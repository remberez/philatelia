import { api } from './api';

const authService = {
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
      const response = await api.post('/auth/login', {
        email,
        password,
      });

      const { access_token } = response.data;

      if (access_token) {
        localStorage.setItem('token', access_token);
        return response.data;
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
      const response = await api.get("/users/me");
      return response.data;
    } catch (error) {
      console.error("Error fetching user data:", error);
      throw new Error("Failed to fetch user data");
    }
  }
};

export default authService;
