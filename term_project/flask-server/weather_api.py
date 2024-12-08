from flask import Flask, request, jsonify
import requests

app = Flask(__name__)

@app.route('/get_weather', methods=['POST'])
def get_weather():
    data = request.json
    latitude = data['latitude']
    longitude = data['longitude']

    # 기상청 API 요청 예시
    response = requests.get(f"YOUR_WEATHER_API_URL?lat={latitude}&lon={longitude}")
    weather_data = response.json()
    
    # 예시 로직: 추천 옷 결정
    temperature = weather_data.get('temp', 0)
    if temperature < 10:
        recommendation = {"top": "패딩", "bottom": "기모 바지"}
    else:
        recommendation = {"top": "셔츠", "bottom": "청바지"}
    
    return jsonify({
        "temperature": temperature,
        "recommendation": recommendation
    })

if __name__ == '__main__':
    app.run(debug=True)
