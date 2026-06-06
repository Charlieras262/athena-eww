#!/usr/bin/env python3
import json
import urllib.request
import os
from datetime import datetime, date

API_KEY = "YOUR_API_KEY"
CITY = "YOUR_CITY"
CACHE_FILE = os.path.expanduser("~/.cache/eww_weather_cache.json")

FALLBACK_DATA = {
    "location": "Unknown",
    "temp": "0",
    "desc": "Unknown",
    "type": "day",
    "humidity": "0",
    "wind": "0",
    "forecast": [],
    "sunrise": "--:--",
    "sunset": "--:--",
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


def get_weather_icon(desc):
    desc = desc.lower()
    if any(x in desc for x in ["clear", "sunny"]):
        return ""
    elif any(x in desc for x in ["few clouds", "scattered", "broken", "partly"]):
        return ""
    elif any(x in desc for x in ["cloudy", "overcast", "clouds"]):
        return ""
    elif any(x in desc for x in ["drizzle", "light rain"]):
        return ""
    elif any(x in desc for x in ["thunderstorm"]):
        return "󰖓"
    elif any(x in desc for x in ["snow", "sleet", "blizzard"]):
        return ""
    elif any(x in desc for x in ["rain", "shower"]):
        return ""
    elif any(x in desc for x in ["mist", "fog", "haze"]):
        return "󰖑"
    return ""


def fetch_current():
    url = f"https://api.openweathermap.org/data/2.5/weather?q={CITY}&units=metric&appid={API_KEY}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "EwwWeatherWidget/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None


def fetch_forecast():
    url = f"https://api.openweathermap.org/data/2.5/forecast?q={CITY}&units=metric&appid={API_KEY}"
    try:
        req = urllib.request.Request(
            url, headers={"User-Agent": "EwwWeatherWidget/1.0"}
        )
        with urllib.request.urlopen(req, timeout=8) as response:
            return json.loads(response.read().decode())
    except Exception:
        return None


def main():
    current_raw = fetch_current()
    forecast_raw = fetch_forecast()

    if not current_raw or not forecast_raw:
        cached = load_cache()
        if cached:
            print(json.dumps(cached))
        else:
            print(json.dumps(FALLBACK_DATA))
        return

    try:
        temp_c = str(round(current_raw["main"]["temp"]))
        humidity = str(current_raw["main"]["humidity"])
        desc = current_raw["weather"][0]["description"].title().strip()
        wind_kmh = str(round(current_raw["wind"]["speed"] * 3.6))
        current_time = current_raw.get("dt", datetime.now().timestamp())
        sunrise_ts = current_raw["sys"]["sunrise"]
        sunset_ts = current_raw["sys"]["sunset"]
        weather_type = "day" if sunrise_ts <= current_time < sunset_ts else "night"

        sunrise = datetime.fromtimestamp(sunrise_ts).strftime("%H:%M")
        sunset = datetime.fromtimestamp(sunset_ts).strftime("%H:%M")

        # Forecast
        today = date.today()
        days = {}
        for item in forecast_raw["list"]:
            dt = datetime.fromtimestamp(item["dt"])
            date_key = dt.strftime("%Y-%m-%d")
            hour = dt.hour
            if date_key not in days or abs(hour - 12) < abs(
                datetime.fromtimestamp(days[date_key]["dt"]).hour - 12
            ):
                days[date_key] = item

        forecast_list = []
        for date_key in sorted(days.keys()):
            item = days[date_key]
            dt = datetime.fromtimestamp(item["dt"])
            if dt.date() == today:
                continue
            f_desc = item["weather"][0]["description"].title()
            f_temp = round(item["main"]["temp"], 1)
            forecast_list.append(
                {
                    "day": dt.strftime("%A"),
                    "date": dt.strftime("%d %b"),
                    "temp": f_temp,
                    "desc": f_desc,
                    "icon": get_weather_icon(f_desc),
                }
            )

        forecast_list = forecast_list[:4]

        output = {
            "location": current_raw.get("name", ""),
            "temp": temp_c,
            "desc": desc,
            "type": weather_type,
            "humidity": humidity,
            "wind": wind_kmh,
            "forecast": forecast_list,
            "sunrise": sunrise,
            "sunset": sunset,
        }

        save_cache(output)
        print(json.dumps(output))

    except (KeyError, IndexError, ValueError):
        cached = load_cache()
        if cached:
            print(json.dumps(cached))
        else:
            print(json.dumps(FALLBACK_DATA))


if __name__ == "__main__":
    main()
