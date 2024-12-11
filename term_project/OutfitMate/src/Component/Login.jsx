import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import styles from "./Login.module.css";

function Login() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [error, setError] = useState("");
  const { login } = useAuth();
  const navigate = useNavigate();

  const handleLogin = (e) => {
    e.preventDefault();
    if (!username || !password) {
      setError("아이디와 비밀번호를 입력해주세요.");
      return;
    }

    if (username === "user" && password === "1234") {
      login();
      navigate("/detail");
    } else {
      setError("아이디 또는 비밀번호가 잘못되었습니다.");
    }
  };

  const goToSignUp = () => {
    navigate("/signup");
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.loginContainer}>
        {/* 왼쪽 설명 컨테이너 */}
        <div className={styles.infoContainer}>
          <h1 className={styles.logoText}>
            <span className={styles.logoPrimary}>Outfit</span>{" "}
            <span className={styles.logoAccent}>Mate</span>
          </h1>

          <p className={styles.descriptionText}>
            날씨와 이미지를 기반으로 완벽한 의상을 추천받고, 자신의 스타일을
            확인해보세요!
          </p>
        </div>

        {/* 오른쪽 로그인 폼 */}
        <div className={styles.formContainer}>
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
            <p className={styles.signUpText}>
              아직 계정이 없으신가요?
              <span className={styles.signUpLink} onClick={goToSignUp}>
                회원가입
              </span>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}

export default Login;
