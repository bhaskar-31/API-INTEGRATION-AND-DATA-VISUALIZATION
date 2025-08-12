# API-INTEGRATION-AND-DATA-VISUALIZATION
*COMPANY:CODETECH IT SOLUTIONS

*NAME:PONNALA BHASKAR

*INTERN:CT04DY696

*DOMAIN:PYTHON PROGRAMMING

*DURATION:4 WEEKS

*MENTOR:NEELA SANTOSH

**DESCRIPTION OF THE TASK

# Weather & Air Quality Visualization (Free API)

##  Overview
This project fetches **hourly temperature** and **PM2.5 air quality** data for any city in the world using **free, no-API-key-required** public data sources. It then visualizes the results on a dual-axis chart using `matplotlib`.

The goal is to demonstrate:
- **API integration** from multiple sources.
- **Data processing** and cleaning in Python.
- **Data visualization** with multiple scales in one plot.

## APIs Used
1. **Nominatim (OpenStreetMap)**  
   - Converts a city name to latitude/longitude (geocoding).
   - No API key required.
   - Requires a valid `User-Agent` header.

2. **Open-Meteo API**  
   - Provides hourly forecasts for temperature, PM2.5, and other parameters.
   - No API key required.
   - Fast and reliable for free public use.

##  Features
- Accepts **any city name** as input.
- Geocodes location automatically.
- Fetches **48 hours of hourly forecasts** for:
  - Temperature (°C)
  - PM2.5 (µg/m³)
- Displays a **dual-axis plot**:
  - Left axis: Temperature (°C) — solid blue line.
  - Right axis: PM2.5 — dashed orange line.
- Works entirely without paid services.

##OUTPUT

<img width="351" height="27" alt="Image" src="https://github.com/user-attachments/assets/c548cbab-3d12-4761-a00f-e4c46877d2f4" />

##  Installation
1. Clone or download the repository.
2. Install Python dependencies:
   ```bash

 

