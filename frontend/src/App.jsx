import { Route, Routes } from "react-router-dom"
import MainLayout from "./components/Layout"
import Home from "./components/HomePage"
import userStore from "./stores/userStore";
import { useEffect } from "react";
import authService from "./services/userService";
import LoginPage from "./components/LoginPage";
import ProfilePage from "./components/ProfilePage";

function App() {
  useEffect(() => {
    async function fetchData() {
      if (localStorage.getItem("token")) {
        const userData = await authService.getUser();
        userStore.setUser(userData);
      }
    }

    fetchData();
  }, [])
  return (
    <Routes>
      <Route path="/" element={<MainLayout/>}>
        <Route index element={<Home/>}/>
        <Route path="/login" element={<LoginPage/>}/>
        <Route path="/profile" element={<ProfilePage/>}/>
      </Route>
    </Routes>
  )
}

export default App
