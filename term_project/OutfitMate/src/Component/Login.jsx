import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import styles from "./Login.module.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("아이디와 비밀번호를 입력해주세요.");
      return;
    }
    navigate("/detail");
  };

  return (
    <div className={styles.loginContainer}>
      <h2 className={styles.title}>로그인</h2>
      <form onSubmit={handleLogin} className={styles.loginForm}>
        <div className={styles.formGroup}>
          <label htmlFor="username">아이디</label>
          <input
            type="text"
            id="username"
            value={username}
            onChange={(e) => setUsername(e.target.value)}
            placeholder="아이디를 입력하세요"
            required
          />
        </div>
        <div className={styles.formGroup}>
          <label htmlFor="password">비밀번호</label>
          <input
            type="password"
            id="password"
            value={password}
            onChange={(e) => setPassword(e.target.value)}
            placeholder="비밀번호를 입력하세요"
            required
          />
        </div>
        {error && <p className={styles.error}>{error}</p>}
        <button type="submit" className={styles.loginButton}>
          로그인
        </button>
      </form>
    </div>
  );
}

export default Login;
