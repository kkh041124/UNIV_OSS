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
from sklearn.model_selection import train_test_split
from imblearn.over_sampling import SMOTE

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
    
    # 컬럼 이름 변경 및 결측값 처리
    column_mapping = {'Item Purchased': '품목', 'Category': '카테고리', 'Color': '컬러', 'Season': '날씨'}
    data.rename(columns=column_mapping, inplace=True)
    data['온도'] = 20
    data['강수량'] = 0
    return data

def train_models(data):
    top_data = data[data['품목'].str.contains('shirt|sweater', case=False, na=False)]
    bottom_data = data[data['품목'].str.contains('pants|jeans|skirt', case=False, na=False)]
    
    # Label Encoding
    le_color = LabelEncoder()
    le_top = LabelEncoder()
    le_bottom = LabelEncoder()

    top_data['컬러'] = le_color.fit_transform(top_data['컬러'])
    bottom_data['컬러'] = le_color.transform(bottom_data['컬러'])

    # Train-Test Split
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

# 모델 학습
data = load_and_preprocess_data(file_path1, file_path2)
top_model, bottom_model, le_top, le_bottom = train_models(data)


# 1. 날씨 API와 AI 모델 통합
@app.route("/get_weather", methods=["POST"])
def get_weather():
    try:
        data = request.json
        latitude = data.get("latitude", 55)
        longitude = data.get("longitude", 127)

        # 기상청 API 호출
        weather_api_url = (
            f"http://apis.data.go.kr/1360000/VilageFcstInfoService_2.0/getUltraSrtNcst"
            f"?serviceKey={SERVICE_KEY_ENCODED}&pageNo=1&numOfRows=1000&dataType=JSON"
            f"&base_date=20241208&base_time=1200&nx={latitude}&ny={longitude}"
        )
        response = requests.get(weather_api_url)
        if response.status_code == 200:
            weather_data = response.json()
            temp = float(weather_data['response']['body']['items']['item'][0]['obsrValue'])  # 온도 값 예시
            
            # AI 모델 예측
            input_data = pd.DataFrame([[0, temp, 0]], columns=['컬러', '온도', '강수량'])
            top_prediction = top_model.predict(input_data)
            bottom_prediction = bottom_model.predict(input_data)

            top_result = le_top.inverse_transform(top_prediction)[0]
            bottom_result = le_bottom.inverse_transform(bottom_prediction)[0]
            
            return jsonify({"temperature": temp, "recommendation": {"top": top_result, "bottom": bottom_result}})
        return jsonify({"error": "날씨 데이터를 가져올 수 없습니다."}), 500
    except Exception as e:
        return jsonify({"error": str(e)}), 500


# 2. 스마트 의상 피팅 API
@app.route("/fit_clothes", methods=["POST"])
def fit_clothes():
    try:
        user_image = request.files['user_image']
        clothes_image = request.files['clothes_image']
        
        # 이미지 열기
        user_img = Image.open(user_image).convert("RGBA")
        clothes_img = Image.open(clothes_image).convert("RGBA")
        
        # 간단한 이미지 병합 예제 (AI 모델로 대체 가능)
        user_array = np.array(user_img)
        clothes_array = np.array(clothes_img)
        combined_img = cv2.addWeighted(user_array, 0.7, clothes_array, 0.3, 0)
        
        # 결과 이미지 반환
        result_img = Image.fromarray(combined_img)
        img_io = io.BytesIO()
        result_img.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")

    except Exception as e:
        return jsonify({"error": str(e)}), 500


if __name__ == "__main__":
    app.run(debug=True, port=5000)
