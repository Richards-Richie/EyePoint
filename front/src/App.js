import React from "react";
import { Routes, Route } from "react-router-dom";
import Main from "./pages/Landingpage/Main";
import Login from "./pages/Loginpage/Login";
import RegisterPage from "./pages/Registerpage/Registerpage";
import VideoComponent from "./components/VideoComponent";
import "./appstyle.css";
import Resetpg from "./pages/Resetpage/Resetpg";

function App() {
  return (
    <Routes>
      <Route path="/" element={<Main />} />
      <Route path="/login" element={<Login />} />
      <Route path="/register" element={<RegisterPage />} />
      <Route path="/eyepoint" element={<VideoComponent />} />
      <Route path="/reset_password" element={<Resetpg />} />
    </Routes>
  );
}

export default App;
