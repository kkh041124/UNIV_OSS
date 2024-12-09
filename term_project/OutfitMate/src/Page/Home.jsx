import React, { useRef, useEffect } from "react";
import { useNavigate } from "react-router-dom";
import { useLocation } from "react-router-dom";

import styles from "./Home.module.css";
import React_icon from "./Static/React-ico.png";
import flask_icon from "./Static/flask.png";
import opcv_icon from "./Static/opencv-icon.png";
import github_icon from "./Static/github-mark.svg";
import css_icon from "./Static/css-modules-logo.png";
import pandaImage from "./Static/panda-image.png";
import testVideo from "./Static/test.mp4";
import playButton from "./Static/play-button.png"; // 플레이 버튼 이미지
import location_icon from "./Static/location-icon.png";
import folder_icon from "./Static/folder.png";
import ImageSelector from "../Component/ImageSelector";

function Home() {
  const navigate = useNavigate();
  const videoRef = useRef(null);

  const goToSignUp = () => navigate("/signup");
  const goToLogin = () => navigate("/login");
  const goToDetailPage = () => navigate("/detail");

  const handlePlayVideo = () => {
    if (videoRef.current) {
      videoRef.current.play();
    }
  };

  // "정보" 버튼 클릭 시 videoSection으로 스크롤
  const goToInfoSection = () => {
    const videoSection = document.getElementById("videoSection");
    if (videoSection) {
      videoSection.scrollIntoView({ behavior: "smooth" });
    }
  };

  // "FAQ" 버튼 클릭 시 faqSection으로 스크롤
  const goToFAQSection = () => {
    const faqSection = document.getElementById("faqSection");
    if (faqSection) {
      faqSection.scrollIntoView({ behavior: "smooth" });
    }
  };
  const location = useLocation();

  useEffect(() => {
    if (location.state?.scrollTo) {
      const target = document.getElementById(location.state.scrollTo);
      if (target) {
        target.scrollIntoView({ behavior: "smooth" });
      }
    }
  }, [location]);

  return (
    <div className={styles.homeContainer}>
      <header className={styles.header}>
        <nav>
          <button className={styles.navButton} onClick={goToInfoSection}>
            정보
          </button>
          <button className={styles.navButton} onClick={goToFAQSection}>
            FAQ
          </button>
          <button className={styles.navButton} onClick={goToSignUp}>
            로그인
          </button>
        </nav>
      </header>

      <div className={styles.contentContainer}>
        <div className={styles.textContainer}>
          <h1 className={styles.title}>Outfit Mate</h1>
          <p className={styles.subtitle}>
            오늘의 날씨, 당신의 옷장을 스마트하게 바꿔보세요!
          </p>
          <p className={styles.description}>
            내 위치와 이미지만으로, 원하는 스타일을 손쉽게 만들어 보세요!
          </p>
          <button className={styles.startButton} onClick={goToDetailPage}>
            시작하기
          </button>
          <div className={styles.logoContainer}>
            <img
              src={React_icon}
              alt="React"
              className={`${styles.logo} ${styles.icon1}`}
            />
            <img
              src={flask_icon}
              alt="Flask"
              className={`${styles.logo} ${styles.icon2}`}
            />
            <img
              src={opcv_icon}
              alt="OpenCV"
              className={`${styles.logo} ${styles.icon3}`}
            />
            <img
              src={css_icon}
              alt="CSS Modules"
              className={`${styles.logo} ${styles.icon4}`}
            />
            <img
              src={github_icon}
              alt="GitHub"
              className={`${styles.logo} ${styles.icon5}`}
            />
          </div>
        </div>

        <div className={styles.imageContainer}>
          <img
            src={pandaImage}
            alt="Outfit Try-On"
            className={styles.pandaImage}
          />
        </div>
      </div>

      {/* id 부여: 정보 버튼 클릭 시 이동할 영역 */}
      <div className={styles.videoContainer} id="videoSection">
        <h2 className={styles.videoTitle}>Outfit Mate는 어떤 서비스인가요?</h2>
        <div className={styles.videoWrapper}>
          <video ref={videoRef} controls className={styles.video}>
            <source src={testVideo} type="video/mp4" />
            지원하지 않는 브라우저입니다.
          </video>
          <button className={styles.playButton} onClick={handlePlayVideo}>
            <img src={playButton} alt="Play Button" />
          </button>
        </div>
        <p className={styles.videoDescription}>
          OutfitMate는 사용자가 날씨와 이미지 정보를 바탕으로 쉽고 빠르게 맞춤형
          옷 추천과 웹캠을 통한 의상 입히기 기능을 경험할 수 있는 웹 기반
          도구입니다. 참고:{" "}
          <a
            href="https://github.com/kkh041124/UNIV_OSS"
            target="_blank"
            rel="noopener noreferrer"
          >
            여기에서 OutfitMate를 살펴보세요
          </a>
        </p>
      </div>

      <div className={styles.howToUseContainer}>
        <h2 className={styles.howToUseTitle}>어떻게 사용하나요?</h2>
        <div className={styles.stepsContainer}>
          {/* Step 1 */}
          <div className={styles.step}>
            <img
              src={location_icon}
              alt="Location"
              className={styles.stepIcon}
            />
            <p className={styles.stepDescription}>
              <strong>1. 위치 불러오기</strong>
              <br />
              자신의 사는 지역의 날씨를 이용하여 날씨별 옷 추천을 받아보세요!
            </p>
          </div>

          {/* Step 2 */}
          <div className={styles.step}>
            <img src={folder_icon} alt="Upload" className={styles.stepIcon} />
            <p className={styles.stepDescription}>
              <strong>2. 웹캠이나 사진을 불러오세요</strong>
              <br />
              자신의 상체의 사진을 찍거나 사진을 올려주세요!
            </p>
          </div>

          {/* Step 3 */}
          <div className={styles.step}>
            <button
              className={styles.resultButton}
              onClick={() => alert("시작하기를 눌러보세요!")}
            >
              결과보기
            </button>
            <p className={styles.stepDescription}>
              <strong>3. 결과보기</strong>
              <br />
              결과보기 버튼을 눌러 옷과 자신이 어울리는 지 확인해 주세요!
            </p>
          </div>
        </div>
      </div>

      {/* Image Selector */}
      <div className={styles.selectorContainer}>
        <ImageSelector />
      </div>

      {/* FAQ 섹션에 id 부여: FAQ 버튼 클릭 시 이동할 영역 */}
      <div className={styles.faqContainer} id="faqSection">
        <h2 className={styles.faqTitle}>자주 묻는 질문 (FAQ)</h2>
        <div className={styles.faqItem}>
          <h3>Q1. Outfit Mate는 무엇인가요?</h3>
          <p>
            Outfit Mate는 사용자가 날씨와 이미지를 바탕으로 맞춤형 의상을
            추천하고 시뮬레이션할 수 있는 스마트 도구입니다.
          </p>
        </div>
        <div className={styles.faqItem}>
          <h3>Q2. 어떻게 사용하면 되나요?</h3>
          <p>
            1. 위치를 불러와 날씨를 확인하고, 2. 웹캠이나 사진을 업로드한 뒤,
            결과를 확인하시면 됩니다.
          </p>
        </div>
        <div className={styles.faqItem}>
          <h3>Q3. 어떤 사진을 업로드해야 하나요?</h3>
          <p>상체가 보이는 사진을 업로드하시면 더 정확한 추천이 가능합니다.</p>
        </div>
        <div className={styles.faqItem}>
          <h3>Q4. 비용이 발생하나요?</h3>
          <p>Outfit Mate는 무료로 제공되며 누구나 사용할 수 있습니다.</p>
        </div>
      </div>

      <footer className={styles.footer}>
        <div className={styles.footerContent}>
          <p>&copy; 2024 Outfit Mate. All rights reserved.</p>
          <p>
            Designed and developed by{" "}
            <a
              href="https://github.com/kkh041124/UNIV_OSS"
              target="_blank"
              rel="noopener noreferrer"
            >
              OutfitMate Team
            </a>
          </p>
        </div>
      </footer>
    </div>
  );
}

export default Home;
