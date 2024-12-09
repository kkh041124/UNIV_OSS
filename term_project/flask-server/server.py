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


@app.route("/fit_clothes", methods=["POST"])
def fit_clothes():
    try:
        user_image = request.files['user_image']
        clothes_image = request.files['clothes_image']
        
        user_img = Image.open(user_image).convert("RGBA")
        clothes_img = Image.open(clothes_image).convert("RGBA")
        
        user_array = np.array(user_img)
        clothes_array = np.array(clothes_img)
        combined_img = cv2.addWeighted(user_array, 0.7, clothes_array, 0.3, 0)
        
        result_img = Image.fromarray(combined_img)
        img_io = io.BytesIO()
        result_img.save(img_io, "PNG")
        img_io.seek(0)
        return send_file(img_io, mimetype="image/png")
    except Exception as e:
        print(f"Error: {str(e)}")
        return jsonify({"error": str(e)}), 500

if __name__ == "__main__":
    app.run(debug=True, port=5000)
