import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import { useAuth } from "../AuthContext";
import styles from "./SignUp.module.css";

function SignUp() {
  const [username, setUsername] = useState("");
  const [password, setPassword] = useState("");
  const [confirmPassword, setConfirmPassword] = useState("");
  const [error, setError] = useState("");
  const { signup } = useAuth();
  const navigate = useNavigate();

  const handleSignUp = (e) => {
    e.preventDefault();
    if (password !== confirmPassword) {
      setError("비밀번호가 일치하지 않습니다.");
      return;
    }
    signup();
    navigate("/");
  };

  return (
    <div className={styles.pageContainer}>
      <div className={styles.signUpContainer}>
        {/* 설명 컨테이너 */}
        <div className={styles.infoContainer}>
          <h1 className={styles.logoText}>
            <span className={styles.logoPrimary}>Outfit</span>{" "}
            <span className={styles.logoAccent}>Mate</span>
          </h1>
          <p className={styles.descriptionText}>
            당신만의 스타일을 완성하세요! Outfit Mate가 날씨와 이미지를 기반으로
            맞춤형 의상을 추천합니다.
          </p>
        </div>

        {/* 회원가입 폼 */}
        <div className={styles.formContainer}>
          <h2 className={styles.title}>회원가입</h2>
          <form onSubmit={handleSignUp} className={styles.formInner}>
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
            <div className={styles.formGroup}>
              <label htmlFor="confirmPassword">비밀번호 확인</label>
              <input
                type="password"
                id="confirmPassword"
                value={confirmPassword}
                onChange={(e) => setConfirmPassword(e.target.value)}
                placeholder="비밀번호를 확인하세요"
                required
              />
            </div>
            {error && <p className={styles.error}>{error}</p>}
            <button type="submit" className={styles.signUpButton}>
              회원가입
            </button>
            <p className={styles.loginText}>
              이미 계정이 있으신가요?{" "}
              <span
                className={styles.loginLink}
                onClick={() => navigate("/login")}
              >
                로그인
              </span>
            </p>
          </form>
        </div>
      </div>
    </div>
  );
}

export default SignUp;
