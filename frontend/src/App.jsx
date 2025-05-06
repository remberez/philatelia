import { Route, Routes } from "react-router-dom"
import MainLayout from "./components/Layout"
import Home from "./components/HomePage"

function App() {
  return (
    <Routes>
      <Route path="/" element={<MainLayout/>}>
        <Route index element={<Home/>}/>
      </Route>
    </Routes>
  )
}

export default App
