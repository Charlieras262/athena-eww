#!/usr/bin/env python3
import json
import urllib.request
import os
from datetime import datetime

API_KEY = "YOUR_API_KEY"
LAT = "YOUR_LATITUDE"
LON = "YOUR_LONGITUDE"
CACHE_FILE = os.path.expanduser("~/.cache/eww_weather_cache.json")

FALLBACK_DATA = {
    "location": "",
    "temp": "0",
    "desc": "Unknown",
    "type": "day",
    "humidity": "0",
    "wind": "0",
}


def load_cache():
    if os.path.exists(CACHE_FILE):
        try:
            with open(CACHE_FILE, "r") as f:
                return json.load(f)
        except Exception:
            return None
    return None


def save_cache(data):
    try:
        os.makedirs(os.path.dirname(CACHE_FILE), exist_ok=True)
        with open(CACHE_FILE, "w") as f:
            json.dump(data, f)
    except Exception:
        pass


def fetch_openweathermap():
    url = f"https://api.openweathermap.org/data/2.5/weather?lat={LAT}&lon={LON}&units=metric&appid={API_KEY}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "EwwWeatherWidget/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None


def main():
    raw_data = fetch_openweathermap()

    if not raw_data or "main" not in raw_data:
        cached_output = load_cache()
        if cached_output:
            print(json.dumps(cached_output))
        else:
            print(json.dumps(FALLBACK_DATA))
        return

    try:
        temp_c = str(round(raw_data["main"]["temp"]))
        humidity = str(raw_data["main"]["humidity"])

        weather_info = raw_data["weather"][0]
        desc = weather_info["description"].title().strip()

        wind_ms = raw_data["wind"]["speed"]
        wind_kmh = str(round(wind_ms * 3.6))

        current_time = raw_data.get("dt", datetime.now().timestamp())
        sunrise = raw_data["sys"]["sunrise"]
        sunset = raw_data["sys"]["sunset"]

        if sunrise <= current_time < sunset:
            weather_type = "day"
        else:
            weather_type = "night"

        output = {
            "location": "",
            "temp": temp_c,
            "desc": desc,
            "type": weather_type,
            "humidity": humidity,
            "wind": wind_kmh,
        }

        save_cache(output)
        print(json.dumps(output))

    except (KeyError, IndexError, ValueError):
        cached_output = load_cache()
        if cached_output:
            print(json.dumps(cached_output))
        else:
            print(json.dumps(FALLBACK_DATA))


if __name__ == "__main__":
    main()
