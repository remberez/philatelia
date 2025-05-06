import { Route, Routes } from "react-router-dom"
import MainLayout from "./components/Layout"
import Home from "./components/HomePage"
import userStore from "./stores/userStore";
import { useEffect } from "react";
import authService from "./services/userService";

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
      </Route>
    </Routes>
  )
}

export default App
