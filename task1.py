"""
free_api_multi_viz.py

Uses:
 - Nominatim (OpenStreetMap) to geocode a city name -> lat/lon (no API key)
 - Open-Meteo to fetch hourly temperature and PM2.5 forecast (no API key)
 - Plots temperature and PM2.5 on a single matplotlib figure

Install requirements:
    pip install requests matplotlib python-dateutil
"""

import requests
from dateutil import parser
import matplotlib.pyplot as plt
from datetime import datetime
import sys

HEADERS = {"User-Agent": "free-api-demo-script/1.0 (+your_email@example.com)"}

def geocode_city(city_name):
    url = "https://nominatim.openstreetmap.org/search"
    params = {"q": city_name, "format": "json", "limit": 1}
    resp = requests.get(url, params=params, headers=HEADERS, timeout=10)
    resp.raise_for_status()
    results = resp.json()
    if not results:
        raise ValueError(f"Could not find location for '{city_name}'")
    loc = results[0]
    return float(loc["lat"]), float(loc["lon"]), loc.get("display_name", city_name)

def fetch_open_meteo(lat, lon, hours=48):
    """
    Fetch hourly temperature and PM2.5 for the next `hours` hours.
    Open-Meteo supports hourly variables like temperature_2m and pm2_5.
    """
    # Determine the hourly variables we want
    hourly_vars = "temperature_2m,pm2_5"
    # Build request - we ask for timezone=auto to get local times
    url = "https://api.open-meteo.com/v1/forecast"
    params = {
        "latitude": lat,
        "longitude": lon,
        "hourly": hourly_vars,
        "forecast_days": 3,   # few days so we have enough hours
        "timezone": "auto"
    }
    resp = requests.get(url, params=params, timeout=10)
    resp.raise_for_status()
    return resp.json()

def prepare_series(meteo_json, max_hours=48):
    times = meteo_json["hourly"]["time"]
    temps = meteo_json["hourly"].get("temperature_2m", [])
    pm25 = meteo_json["hourly"].get("pm2_5", [])

    # convert times to datetimes and slice to max_hours
    dt_times = [parser.isoparse(t) for t in times]
    dt_times = dt_times[:max_hours]
    temps = temps[:max_hours] if temps else []
    pm25 = pm25[:max_hours] if pm25 else []

    return dt_times, temps, pm25

def plot_temp_and_pm25(times, temps, pm25, place_name):
    fig, ax1 = plt.subplots(figsize=(12,6))

    # Temperature on left y-axis
    ax1.plot(times, temps, marker='o', label='Temperature (°C)')
    ax1.set_xlabel('Local Date & Time')
    ax1.set_ylabel('Temperature (°C)')
    ax1.tick_params(axis='x', rotation=45)
    ax1.grid(True, which='both', linestyle='--', alpha=0.3)

    # PM2.5 on right y-axis
    ax2 = ax1.twinx()
    ax2.plot(times, pm25, marker='s', linestyle='--', label='PM2.5 (µg/m³)')
    ax2.set_ylabel('PM2.5 (µg/m³)')

    # Combine legends
    lines_1, labels_1 = ax1.get_legend_handles_labels()
    lines_2, labels_2 = ax2.get_legend_handles_labels()
    ax1.legend(lines_1 + lines_2, labels_1 + labels_2, loc='upper left')

    plt.title(f"Temperature & PM2.5 Forecast — {place_name}")
    plt.tight_layout()
    plt.show()

def main(city_name):
    try:
        lat, lon, display_name = geocode_city(city_name)
        print(f"Location found: {display_name} -> lat={lat}, lon={lon}")

        meteo = fetch_open_meteo(lat, lon)
        times, temps, pm25 = prepare_series(meteo, max_hours=48)

        if not temps:
            print("Warning: temperature data not found in response.")
        if not pm25:
            print("Warning: PM2.5 data not found in response.")

        plot_temp_and_pm25(times, temps, pm25, display_name)
    except Exception as e:
        print("Error:", str(e))

if __name__ == "__main__":
    if len(sys.argv) >= 2:
        city = " ".join(sys.argv[1:])
    else:
        city = input("Enter city name (e.g. Delhi, Mumbai, London): ").strip()
    main(city)
