import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import styles from "./Login.module.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth(); // AuthContext에서 로그인 함수 사용
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("아이디와 비밀번호를 입력해주세요.");
      return;
    }

    // 실제 인증 로직은 여기에 추가해야 함 (예: API 호출)
    if (username === "user" && password === "1234") {
      login(); // 로그인 상태 업데이트
      navigate("/detail"); // 로그인 성공 시 Detail 페이지로 이동
    } else {
      setError("아이디 또는 비밀번호가 잘못되었습니다.");
    }
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
