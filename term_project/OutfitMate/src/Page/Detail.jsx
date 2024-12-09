import React, { useState } from "react";
import { useNavigate } from "react-router-dom";

import axios from "axios";
import styles from "./Detail.module.css";

// 날씨 아이콘 import (전부 ./Static/weather_images 경로로 변경)
import NB01 from "./Static/weather_images/NB01.png";
import NB01_N from "./Static/weather_images/NB01_N.png";
import NB02 from "./Static/weather_images/NB02.png";
import NB02_N from "./Static/weather_images/NB02_N.png";
import NB03 from "./Static/weather_images/NB03.png";
import NB03_N from "./Static/weather_images/NB03_N.png";
import NB04 from "./Static/weather_images/NB04.png";
import NB07 from "./Static/weather_images/NB07.png";
import NB08 from "./Static/weather_images/NB08.png";
import NB20 from "./Static/weather_images/NB20.png";
import NB11 from "./Static/weather_images/NB11.png";
import NB22 from "./Static/weather_images/NB22.png";
import NB12 from "./Static/weather_images/NB12.png";
import NB13 from "./Static/weather_images/NB13.png";
import NB23 from "./Static/weather_images/NB23.png";
import NB14 from "./Static/weather_images/NB14.png";
import NB18 from "./Static/weather_images/NB18.png";
import NB15 from "./Static/weather_images/NB15.png";
import NB17 from "./Static/weather_images/NB17.png";
import NB16 from "./Static/weather_images/NB16.png";

// 기본 아이콘(기본은 NB01로 사용)
const WEATHER_DEFAULT = NB01;

function Detail() {
  const [weather, setWeather] = useState({});
  const [recommendation, setRecommendation] = useState({});
  const [location, setLocation] = useState(null);
  const [userImage, setUserImage] = useState(null);
  const [clothesImage, setClothesImage] = useState(null);
  const [resultImage, setResultImage] = useState(null);
  const navigate = useNavigate(); // useNavigate 훅 초기화

  // 날씨 상태 코드에 따른 아이콘 매핑 함수
  const getWeatherIcon = () => {
    if (!weather || !weather.conditionCode) {
      return WEATHER_DEFAULT;
    }

    switch (weather.conditionCode) {
      case 1: // 맑음(낮)
        return NB01;
      case 2: // 맑음(밤)
        return NB01_N;
      case 3: // 구름조금(낮)
        return NB02;
      case 4: // 구름조금(밤)
        return NB02_N;
      case 5: // 구름많음(낮)
        return NB03;
      case 6: // 구름많음(밤)
        return NB03_N;
      case 7: // 흐림
        return NB04;
      case 8: // 소나기
        return NB07;
      case 9: // 비
        return NB08;
      case 10: // 가끔 비, 한때 비
        return NB20;
      case 11: // 눈
        return NB11;
      case 12: // 가끔 눈, 한때 눈
        return NB22;
      case 13: // 비 또는 눈
        return NB12;
      case 14: // 가끔 비 또는 눈
        return NB22;
      case 15: // 눈 또는 비
        return NB13;
      case 16: // 가끔 눈 또는 비
        return NB23;
      case 17: // 천둥번개
        return NB14;
      case 18: // 연무
        return NB18;
      case 19: // 안개
        return NB15;
      case 20: // 박무(엷은 안개)
        return NB17;
      case 21: // 황사
        return NB16;
      default:
        return WEATHER_DEFAULT;
    }
  };

  // 날씨 데이터 호출
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

  // 의상 피팅 API 호출
  const handleFitClothes = async () => {
    const formData = new FormData();
    formData.append("user_image", userImage);
    formData.append("clothes_image", clothesImage);

    try {
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
    }
  };
  const navigateToHomeSection = (section) => {
    navigate("/", { state: { scrollTo: section } });
  };
  // 현재 날짜와 시간 포맷
  const now = new Date();
  const year = now.getFullYear();
  const month = String(now.getMonth() + 1).padStart(2, "0");
  const day = String(now.getDate()).padStart(2, "0");
  const hours = String(now.getHours()).padStart(2, "0");
  const minutes = String(now.getMinutes()).padStart(2, "0");
  const formattedDate = `${year}년 ${month}월 ${day}일 ${hours}:${minutes}`;

  return (
    <div className={styles.detailContainer}>
      <div className={styles.header}>
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
        <button className={styles.headerButton}>로그인</button>
      </div>
      {/* 왼쪽 컬럼 */}
      <div className={styles.leftContainer}>
        <div className={styles.dateTimeBox}>{formattedDate}</div>
        <div className={styles.weatherBox}>
          <div className={styles.weatherIcon}>
            <img src={getWeatherIcon()} alt="날씨 아이콘" />
          </div>
          <div className={styles.weatherInfo}>
            {weather.temperature ? (
              <div>
                <p>현재 온도 : {weather.temperature}°C</p>
              </div>
            ) : (
              <p>현재 온도 : --°C</p>
            )}
          </div>
          <div className={styles.locationInfo}>
            {location ? (
              <p>
                관측 지점 : 위도 {location.latitude}, 경도 {location.longitude}
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
          <p>상의 : {recommendation.top ? recommendation.top : "~~"}</p>
          <p>하의 : {recommendation.bottom ? recommendation.bottom : "~~"}</p>
        </div>
      </div>

      {/* 오른쪽 컬럼 */}
      <div className={styles.rightContainer}>
        <div className={styles.resultTitle}>옷 입한 결과물 보여주는 창</div>
        <div className={styles.resultButtons}>
          <button className={styles.showResultButton}>결과보기</button>
          {/* 필요하다면 icon 파일을 import해서 사용하거나, 이모지를 대신하여 icon 이미지 사용 */}
          <button className={styles.iconButton}>📁</button>
          <button className={styles.iconButton}>📷</button>
        </div>
        {resultImage && (
          <img
            src={resultImage}
            alt="Fitted Clothes"
            className={styles.resultImage}
          />
        )}
      </div>
    </div>
  );
}

export default Detail;
