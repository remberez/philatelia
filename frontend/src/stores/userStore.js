import { makeAutoObservable } from "mobx";

class UserStore {
  user = null;
  isAuth = false;

  constructor() {
    makeAutoObservable(this);
  }

  setUser(user) {
    this.user = user;
    this.isAuth = true;
  }

  logout() {
    this.user = null;
    this.isAuth = false;
    localStorage.removeItem("token");
  }

  setAuthStatus(status) {
    this.isAuth = status;
  }
}

const userStore = new UserStore();
export default userStore;
