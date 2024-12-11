from flask import Flask, request, jsonify, send_file
from flask_cors import CORS
from PIL import Image
import numpy as np
import pandas as pd
import cv2
import requests
import io
from urllib.parse import quote
from sklearn.ensemble import RandomForestClassifier
from sklearn.preprocessing import LabelEncoder
from imblearn.over_sampling import SMOTE
import xml.etree.ElementTree as ET
from datetime import datetime, timedelta
from pyproj import Proj
import mediapipe as mp

app = Flask(__name__)
CORS(app)

# 기상청 서비스 키
SERVICE_KEY_DECODED = "b1tZLYY9n9j+abXg7IAiQZoDQUe1zy2yel/NuPrIB59sdXUPVEdp5z5Wj6wTFGU/NotP3nwvunTDNVhdJRAJ3w=="
SERVICE_KEY_ENCODED = quote(SERVICE_KEY_DECODED)

# 학습된 모델 불러오기
file_path1 = "./data/shopping_trends.csv"
file_path2 = "./data/shopping_trends_updated.csv"

def load_and_preprocess_data(file_path1, file_path2):
    data1 = pd.read_csv(file_path1)
    data2 = pd.read_csv(file_path2)
    data = pd.concat([data1, data2], ignore_index=True)
    column_mapping = {'Item Purchased': '품목', 'Category': '카테고리', 'Color': '컬러', 'Season': '날씨'}
    data.rename(columns=column_mapping, inplace=True)
    data['온도'] = 20
    data['강수량'] = 0
    return data

def train_models(data):
    top_data = data[data['품목'].str.contains('shirt|sweater', case=False, na=False)]
    bottom_data = data[data['품목'].str.contains('pants|jeans|skirt', case=False, na=False)]
    
    le_color = LabelEncoder()
    le_top = LabelEncoder()
    le_bottom = LabelEncoder()

    top_data['컬러'] = le_color.fit_transform(top_data['컬러'])
    bottom_data['컬러'] = le_color.transform(bottom_data['컬러'])

    X_top = top_data[['컬러', '온도', '강수량']]
    y_top = le_top.fit_transform(top_data['품목'])
    X_bottom = bottom_data[['컬러', '온도', '강수량']]
    y_bottom = le_bottom.fit_transform(bottom_data['품목'])

    smote = SMOTE(random_state=42)
    X_top_res, y_top_res = smote.fit_resample(X_top, y_top)
    X_bottom_res, y_bottom_res = smote.fit_resample(X_bottom, y_bottom)

    top_model = RandomForestClassifier().fit(X_top_res, y_top_res)
    bottom_model = RandomForestClassifier().fit(X_bottom_res, y_bottom_res)
    
    return top_model, bottom_model, le_top, le_bottom

data = load_and_preprocess_data(file_path1, file_path2)
top_model, bottom_model, le_top, le_bottom = train_models(data)

# Lambert Conformal Conic Projection 설정 (기상청 기준)
proj_lambert = Proj(proj='lcc', lat_1=30, lat_2=60, lat_0=38, lon_0=126, x_0=210000, y_0=675000, ellps='WGS84')

def latlon_to_grid(lat, lon):
    """Convert latitude/longitude to KMA grid coordinates (TM projection)."""
    RE = 6371.00877  # Earth's radius (km)
    GRID = 5.0       # Grid spacing (km)
    SLAT1 = 30.0     # Projection standard latitudes
    SLAT2 = 60.0
    OLON = 126.0     # Reference longitude
    OLAT = 38.0      # Reference latitude
    XO = 43          # Reference x-coordinate
    YO = 136         # Reference y-coordinate

    # Conversion logic
    import math
    DEGRAD = math.pi / 180.0
    re = RE / GRID
    slat1 = SLAT1 * DEGRAD
    slat2 = SLAT2 * DEGRAD
    olon = OLON * DEGRAD
    olat = OLAT * DEGRAD

    sn = math.tan(math.pi * 0.25 + slat2 * 0.5) / math.tan(math.pi * 0.25 + slat1 * 0.5)
    sn = math.log(math.cos(slat1) / math.cos(slat2)) / math.log(sn)
    sf = math.tan(math.pi * 0.25 + slat1 * 0.5)
    sf = math.pow(sf, sn) * math.cos(slat1) / sn
    ro = math.tan(math.pi * 0.25 + olat * 0.5)
    ro = re * sf / math.pow(ro, sn)
    ra = math.tan(math.pi * 0.25 + lat * DEGRAD * 0.5)
    ra = re * sf / math.pow(ra, sn)
    theta = lon * DEGRAD - olon
    if theta > math.pi:
        theta -= 2.0 * math.pi
    if theta < -math.pi:
        theta += 2.0 * math.pi
    theta *= sn
    x = (ra * math.sin(theta)) + XO + 0.5
    y = (ro - ra * math.cos(theta)) + YO + 0.5
    return int(x), int(y)

@app.route("/get_weather", methods=["POST"])
def get_weather():
    try:
        data = request.json
        latitude = data.get("latitude", 55)
        longitude = data.get("longitude", 127)

        # Convert lat/lon to grid coordinates
        nx, ny = latlon_to_grid(latitude, longitude)

        # Adjust base date and time dynamically
        now = datetime.now()
        base_date = now.strftime("%Y%m%d")
        base_time = now.strftime("%H00")
        for _ in range(3):  # Retry for the last 3 hours
            weather_api_url = (
                f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
                f"?serviceKey={SERVICE_KEY_ENCODED}&pageNo=1&numOfRows=1000&dataType=XML"
                f"&base_date={base_date}&base_time={base_time}&nx={nx}&ny={ny}"
            )
            response = requests.get(weather_api_url)
            if response.status_code == 200:
                root = ET.fromstring(response.content)
                for item in root.iter("item"):
                    category = item.find("category").text
                    if category == "T1H":
                        temp = float(item.find("obsrValue").text)
                        # AI model prediction
                        input_data = pd.DataFrame([[0, temp, 0]], columns=['컬러', '온도', '강수량'])
                        top_prediction = top_model.predict(input_data)
                        bottom_prediction = bottom_model.predict(input_data)

                        return jsonify({
                            "temperature": temp,
                            "recommendation": {
                                "top": le_top.inverse_transform(top_prediction)[0],
                                "bottom": le_bottom.inverse_transform(bottom_prediction)[0]
                            }
                        })
            base_time = (now - timedelta(hours=1)).strftime("%H00")  # Retry for the previous hour
        return jsonify({"error": "T1H 데이터를 찾을 수 없습니다."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# MediaPipe Pose 초기화
mp_pose = mp.solutions.pose
pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

@app.route("/fit_clothes", methods=["POST"])
def fit_clothes():
    try:
        user_image = request.files.get('user_image', None)
        clothes_image = request.files.get('clothes_image', None)
        
        if user_image is None or clothes_image is None:
            return jsonify({"error": "Please provide both user_image and clothes_image."}), 400

        # 유저 이미지 읽기
        user_img_data = user_image.read()
        if not user_img_data:
            return jsonify({"error": "Failed to read user image."}), 400

        user_img = cv2.imdecode(np.frombuffer(user_img_data, np.uint8), cv2.IMREAD_COLOR)
        if user_img is None:
            return jsonify({"error": "User image is not a valid image."}), 400

        # 의류 이미지 읽기
        clothes_img_data = clothes_image.read()
        if not clothes_img_data:
            return jsonify({"error": "Failed to read clothes image."}), 400

        clothes_img = cv2.imdecode(np.frombuffer(clothes_img_data, np.uint8), cv2.IMREAD_UNCHANGED)
        if clothes_img is None:
            return jsonify({"error": "Clothes image is not a valid image."}), 400

        # MediaPipe Pose 초기화
        mp_pose = mp.solutions.pose
        pose = mp_pose.Pose(static_image_mode=True, min_detection_confidence=0.5)

        # 사용자 이미지에서 Pose Landmarks 추출
        results = pose.process(cv2.cvtColor(user_img, cv2.COLOR_BGR2RGB))
        if not results.pose_landmarks:
            return jsonify({"error": "No pose landmarks found in user image."}), 400

        landmarks = results.pose_landmarks.landmark
        h, w, _ = user_img.shape

        # 랜드마크 인덱스 정의
        LEFT_SHOULDER = mp_pose.PoseLandmark.LEFT_SHOULDER.value
        RIGHT_SHOULDER = mp_pose.PoseLandmark.RIGHT_SHOULDER.value
        NOSE = mp_pose.PoseLandmark.NOSE.value

        # 사용자의 어깨 좌표
        lsh_user = (int(landmarks[LEFT_SHOULDER].x * w), int(landmarks[LEFT_SHOULDER].y * h))
        rsh_user = (int(landmarks[RIGHT_SHOULDER].x * w), int(landmarks[RIGHT_SHOULDER].y * h))

        # 목 포인트 추정 (코와 어깨 라인 사이에서)
        nose_y = int(landmarks[NOSE].y * h)
        shoulders_avg_y = (lsh_user[1] + rsh_user[1]) // 2
        neck_y = (nose_y + shoulders_avg_y) // 2
        neck_x = (lsh_user[0] + rsh_user[0]) // 2
        neck_user = (neck_x, neck_y)

        # 의류 이미지 크기
        ch, cw = clothes_img.shape[:2]

        # 의류 내 어깨, 목 기준점 설정 (해당 의류 이미지에 맞게 조정 가능)
        # 여기서는 가상의 비율 사용: (왼쪽어깨: 30%, 오른쪽어깨: 70%, 위에서 10% 내려온 부분)
        lsh_clothes = (int(cw * 0.3), int(ch * 0.1))
        rsh_clothes = (int(cw * 0.7), int(ch * 0.1))
        neck_clothes = (int(cw * 0.5), 0)  # 최상단 중앙을 목 근처로 가정

        # 어파인 변환을 위한 기준점
        src_points = np.float32([lsh_clothes, rsh_clothes, neck_clothes])
        dst_points = np.float32([lsh_user, rsh_user, neck_user])

        # Affine 변환 행렬 계산
        M = cv2.getAffineTransform(src_points, dst_points)

        # 의류 이미지 변환 적용
        transformed_clothes = cv2.warpAffine(
            clothes_img, M, (w, h),
            flags=cv2.INTER_AREA, borderMode=cv2.BORDER_CONSTANT, borderValue=(0,0,0,0)
        )

        # 변환된 의류 이미지를 사용자 이미지에 합성
        if transformed_clothes.shape[2] == 4:
            # Alpha 채널 분리
            b, g, r, a = cv2.split(transformed_clothes)
            # 마스크 생성 (0~1 스케일)
            mask = a.astype(float) / 255.0
            inv_mask = 1.0 - mask

            for c in range(3):  # B, G, R 각각에 대해 처리
                user_img[:, :, c] = (mask * transformed_clothes[:, :, c] + inv_mask * user_img[:, :, c]).astype(np.uint8)
        else:
            # 알파 채널이 없을 경우, 투명 영역(또는 경계) 처리를 위한 마스크
            gray = cv2.cvtColor(transformed_clothes, cv2.COLOR_BGR2GRAY)
            _, mask_bin = cv2.threshold(gray, 1, 255, cv2.THRESH_BINARY)
            mask_inv = cv2.bitwise_not(mask_bin)

            bg = cv2.bitwise_and(user_img, user_img, mask=mask_inv)
            fg = cv2.bitwise_and(transformed_clothes, transformed_clothes, mask=mask_bin)
            user_img = cv2.add(bg, fg)

        # 결과 이미지를 PNG로 인코딩 후 응답
        _, buffer = cv2.imencode(".png", user_img)
        img_io = io.BytesIO(buffer)
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500




if __name__ == "__main__":
    app.run(debug=True, port=5000)
