import requests

def get_weather(city):
    api_key = "6668f9ade352470096b52840252404"  # Replace with your actual API key
    url = f"http://api.weatherapi.com/v1/current.json?key={api_key}&q={city}"

    response = requests.get(url)
    data = response.json()

    if response.status_code == 200:
        weather = data["current"]["condition"]["text"]  # e.g., Rain, Sunny
        temperature = data["current"]["temp_c"]
        return weather, temperature
    else:
        return None, None
