import React from "react";
import { BrowserRouter as Router, Route, Routes } from "react-router-dom";
import Home from "./Page/Home"; // 수정된 경로
import Login from "./Component/Login";
import SignUp from "./Component/Singup";
import Detail from "./Page/Detail"; // 수정된 경로

function App() {
  return (
    <Router>
      <div className="App">
        <Routes>
          <Route path="/" element={<Home />} />
          <Route path="/login" element={<Login />} />
          <Route path="/signup" element={<SignUp />} />
          <Route path="/detail" element={<Detail />} />
        </Routes>
      </div>
    </Router>
  );
}

export default App;
