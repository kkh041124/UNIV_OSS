import React, { useState } from "react";
import styles from "./Detail.module.css";
import axios from "axios";

function Detail() {
  const [weather, setWeather] = useState({});
  const [recommendation, setRecommendation] = useState({ top: "", bottom: "" });
  const [location, setLocation] = useState({});
  const [image, setImage] = useState(null);

  const fetchWeatherData = async () => {
    navigator.geolocation.getCurrentPosition(async (position) => {
      const { latitude, longitude } = position.coords;
      setLocation({ latitude, longitude });

      try {
        const response = await axios.post("http://127.0.0.1:5000/get_weather", {
          latitude,
          longitude,
        });
        setWeather(response.data);
        setRecommendation(response.data.recommendation);
      } catch (error) {
        console.error("Error fetching weather data:", error);
      }
    });
  };

  return (
    <div className={styles.detailContainer}>
      {/* 상단 날씨 정보 */}
      <div className={styles.weatherSection}>
        <h2>오늘의 날씨</h2>
        <button onClick={fetchWeatherData} className={styles.weatherButton}>
          내 위치 불러오기
        </button>
        {weather.temperature && (
          <div>
            <p>현재 온도: {weather.temperature}°C</p>
            <p>추천 상의: {recommendation.top}</p>
            <p>추천 하의: {recommendation.bottom}</p>
          </div>
        )}
      </div>

      {/* 의상 피팅 결과 */}
      <div className={styles.resultSection}>
        <h2>의상 피팅하기</h2>
        <div className={styles.fileUpload}>
          <label htmlFor="fileInput" className={styles.fileLabel}>
            옷 사진 업로드
          </label>
          <input
            id="fileInput"
            type="file"
            onChange={(e) => setImage(URL.createObjectURL(e.target.files[0]))}
          />
        </div>
        {image && (
          <img
            src={image}
            alt="Fitting Preview"
            className={styles.previewImage}
          />
        )}
      </div>
    </div>
  );
}

export default Detail;
