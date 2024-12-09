import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import { AuthProvider } from "./AuthContext";
import Home from "./Page/Home";
import Login from "./Component/Login";
import Detail from "./Page/Detail";
import SignUp from "./Component/Singup";

function App() {
  return (
    <AuthProvider>
      <Router>
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/detail" element={<Detail />} />
        </Routes>
      </Router>
    </AuthProvider>
  );
}

export default App;
