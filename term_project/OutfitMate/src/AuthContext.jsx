import React, { createContext, useContext, useState } from "react";

// Context 생성
const AuthContext = createContext();

export const AuthProvider = ({ children }) => {
  const [isLoggedIn, setIsLoggedIn] = useState(false);

  const login = () => setIsLoggedIn(true);
  const logout = () => setIsLoggedIn(false);
  const signup = () => setIsLoggedIn(true); // 회원가입 시 로그인 상태로 전환

  return (
    <AuthContext.Provider value={{ isLoggedIn, login, logout, signup }}>
      {children}
    </AuthContext.Provider>
  );
};

export const useAuth = () => useContext(AuthContext);
