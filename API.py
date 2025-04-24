from flask import Flask, jsonify
import requests
import os
import re
import json

app = Flask(__name__)
myapi = "API" 

def parse_location_weather():
    try:
        with open(r"C:\Users\5525\Downloads\Dubai-Bhai\location.txt", "r") as f:
            line = f.readline().strip()
            location, weather = line.split(",")
            return location.strip(), weather.strip()
    except Exception as e:
        print("Error reading location.txt:", e)
        return None, None

def fetch_gemini_recommendations(location, weather):
    prompt = f"""
Given that I am in {location} and the current weather is {weather}, recommend:
- 5 restaurants (for breakfast, lunch, and dinner)
- 5 tourist places
- 5 thrilling activities

Return the data strictly in the following JSON format as a list of objects:
[
  {{
    "image": "https://via.placeholder.com/150",
    "name": "Dubai Mall",
    "pos": "LatLng(25.197197, 55.279797)",
    "type": "Attraction"
  }},
  ...
]
"""

    url = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-2.0-flash:generateContent?key={myapi}"
    headers = {"Content-Type": "application/json"}
    body = {
        "contents": [
            {
                "parts": [{"text": prompt}]
            }
        ]
    }

    response = requests.post(url, headers=headers, json=body)
    try:
        text_response = response.json()["candidates"][0]["content"]["parts"][0]["text"]
    except Exception as e:
        print("Error reading Gemini response:", e)
        return []
    try:
        json_string = re.search(r'\[\s*{.*?}\s*\]', text_response, re.DOTALL).group()
        data = json.loads(json_string)
        return data
    except Exception as e:
        print("Gemini response parsing error:", e)
        print("Raw Gemini response was:", text_response)
        return []

@app.route('/recommendations', methods=['GET'])
def get_recommendations():
    location, weather = parse_location_weather()
    if location != "Dubai":
        return jsonify({"error": "Only Dubai is supported."}), 400
    data = fetch_gemini_recommendations(location, weather)
    return jsonify(data)

if __name__ == '__main__':
    app.run(debug=True,port=6969)
