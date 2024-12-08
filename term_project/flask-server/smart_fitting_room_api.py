from flask import Flask, request, jsonify
from PIL import Image
import numpy as np
import cv2

app = Flask(__name__)

@app.route('/fit_clothes', methods=['POST'])
def fit_clothes():
    uploaded_image = request.files['user_image']
    clothes_image = request.files['clothes_image']
    
    # 이미지 처리 예시 (Pillow 및 OpenCV 사용)
    user_img = Image.open(uploaded_image).convert('RGBA')
    clothes_img = Image.open(clothes_image).convert('RGBA')
    
    # 피팅 결과 이미지 생성 예시
    result_img = np.array(user_img)  # 여기에 스마트 피팅 알고리즘 추가
    
    # 가공된 이미지를 반환
    _, encoded_img = cv2.imencode('.png', result_img)
    return encoded_img.tobytes()

if __name__ == '__main__':
    app.run(debug=True)
