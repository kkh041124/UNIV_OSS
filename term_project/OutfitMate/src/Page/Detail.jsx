import React, { useState } from "react";
import { useNavigate } from "react-router-dom";
import axios from "axios";
import styles from "./Detail.module.css";

// 날씨 아이콘 import
import NB01 from "./Static/weather_images/NB01.png";
import NB01_N from "./Static/weather_images/NB01_N.png";
import { useAuth } from "../AuthContext";

const WEATHER_DEFAULT = NB01;

function Detail() {
  const [weather, setWeather] = useState({});
  const [recommendation, setRecommendation] = useState({});
  const [location, setLocation] = useState(null);
  const [userImage, setUserImage] = useState(null);
  const [clothesImage, setClothesImage] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const [loading, setLoading] = useState(false);
  const navigate = useNavigate();
  const { isLoggedIn, logout } = useAuth();

  const handleLogout = () => {
    logout(); // 로그아웃 상태로 변경
    navigate("/"); // Home 페이지로 이동
  };
  const getWeatherIcon = () => {
    return weather.conditionCode ? NB01 : WEATHER_DEFAULT;
  };

  const fetchWeatherData = async () => {
    navigator.geolocation.getCurrentPosition(async (pos) => {
      const latitude = Math.floor(pos.coords.latitude);
      const longitude = Math.floor(pos.coords.longitude);
      setLocation({ latitude, longitude });

      try {
        const res = await axios.post("http://127.0.0.1:5000/get_weather", {
          latitude,
          longitude,
        });
        setWeather(res.data);
        setRecommendation(res.data.recommendation);
      } catch (error) {
        console.error("Error fetching weather:", error);
      }
    });
  };

  const handleFitClothes = async () => {
    if (!userImage || !clothesImage) {
      alert("사용자 이미지와 의상 이미지를 모두 업로드해주세요.");
      return;
    }

    const formData = new FormData();
    formData.append("user_image", userImage);
    formData.append("clothes_image", clothesImage);

    try {
      setLoading(true);
      const res = await axios.post(
        "http://127.0.0.1:5000/fit_clothes",
        formData,
        {
          responseType: "blob",
        }
      );
      const imageURL = URL.createObjectURL(res.data);
      setResultImage(imageURL);
    } catch (error) {
      console.error("Error fitting clothes:", error);
      alert("의상 피팅 중 문제가 발생했습니다. 다시 시도해주세요.");
    } finally {
      setLoading(false);
    }
  };

  const navigateToHomeSection = (section) => {
    navigate("/", { state: { scrollTo: section } });
  };

  const now = new Date();
  const formattedDate = `${now.getFullYear()}년 ${
    now.getMonth() + 1
  }월 ${now.getDate()}일 ${now.getHours()}:${String(now.getMinutes()).padStart(
    2,
    "0"
  )}`;

  return (
    <div className={styles.detailContainer}>
      {/* Header */}
      <div className={styles.header}>
        {/* 좌측에 로고/타이틀 추가 - 클릭시 홈으로 이동 */}
        <div className={styles.headerLogo} onClick={() => navigate("/")}>
          Outfit Mate
        </div>

        {/* 우측 버튼 영역 */}
        <div className={styles.headerButtons}>
          <button
            className={styles.headerButton}
            onClick={() => navigateToHomeSection("videoSection")}
          >
            정보
          </button>
          <button
            className={styles.headerButton}
            onClick={() => navigateToHomeSection("faqSection")}
          >
            FAQ
          </button>
          <button className={styles.headerButton} onClick={handleLogout}>
            로그아웃
          </button>
        </div>
      </div>

      {/* 왼쪽 컬럼 */}
      <div className={styles.leftContainer}>
        <div className={styles.dateTimeBox}>{formattedDate}</div>
        <div className={styles.weatherBox}>
          <div className={styles.weatherIcon}>
            <img src={getWeatherIcon()} alt="날씨 아이콘" />
          </div>
          <div className={styles.weatherInfo}>
            <p>현재 온도: {weather.temperature || "--"}°C</p>
          </div>
          <div className={styles.locationInfo}>
            {location ? (
              <p>
                위도 {location.latitude}, 경도 {location.longitude}
              </p>
            ) : (
              <p>위치를 불러와 주세요.</p>
            )}
          </div>
        </div>
        <button className={styles.getWeatherButton} onClick={fetchWeatherData}>
          날씨별 옷 추천 받기
        </button>
        <div className={styles.clothesRecommendation}>
          <p>상의: {recommendation.top || "~~"}</p>
          <p>하의: {recommendation.bottom || "~~"}</p>
        </div>
      </div>

      {/* 오른쪽 컬럼 */}
      <div className={styles.rightContainer}>
        {/* 결과 이미지 영역 */}
        {resultImage && (
          <div className={styles.resultImageContainer}>
            <h3>결과 이미지</h3>
            <img
              src={resultImage}
              alt="Fitted Clothes"
              className={styles.resultImage}
            />
          </div>
        )}

        {/* 업로드 영역 */}
        <div className={styles.uploadContainer}>
          <div className={styles.uploadRow}>
            <div className={styles.uploadItem}>
              <label>사용자 이미지:</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setUserImage(e.target.files[0])}
              />
            </div>
            <div className={styles.uploadItem}>
              <label>의상 이미지:</label>
              <input
                type="file"
                accept="image/*"
                onChange={(e) => setClothesImage(e.target.files[0])}
              />
            </div>
          </div>
        </div>

        {/* 결과 버튼 */}
        <button
          className={styles.showResultButton}
          onClick={handleFitClothes}
          disabled={loading}
        >
          {loading ? "처리 중..." : "결과보기"}
        </button>
      </div>
    </div>
  );
}

export default Detail;
