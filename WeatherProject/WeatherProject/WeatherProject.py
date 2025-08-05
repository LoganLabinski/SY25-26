from urllib import request
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent="(Logan Labinski, student, loganlabinski47@gmail.com)")
print("What's your location?")
user_input = input("Enter address: ")
location = geolocator.geocode(user_input)
print(location.address)
print((location.latitude, location.longitude))

import requests # Importing the requests library to make HTTP requests

lat = location.latitude   
lon = location.longitude  


def get_current_weather():
    headers = {"User-Agent": "Logan Labinski (loganlabinski47@gmail.com)"}

    # Step 1: Get station ID for this lat/lon
    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    points_response = requests.get(points_url, headers=headers)
    points_data = points_response.json()

    stations_url = points_data["properties"]["observationStations"]
    stations_response = requests.get(stations_url, headers=headers)
    stations_data = stations_response.json()

    # Use the first station in the list
    station_id = stations_data["features"][0]["properties"]["stationIdentifier"]

    # Step 2: Get the latest observation from this station
    latest_obs_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
    obs_response = requests.get(latest_obs_url, headers=headers)
    obs_data = obs_response.json()

    # Extract weather info
    props = obs_data["properties"]
    temp_c = props["temperature"]["value"]
    temp_f = temp_c * 9/5 + 32 if temp_c is not None else None
    wind_speed = props["windSpeed"]["value"]
    text_desc = props["textDescription"]

    print(f"\nCurrent conditions at {station_id}:")
    if temp_f is not None:
        print(f"Temperature: {temp_f:.1f}F")
    else:
        print("Temperature: Not available")
    print(f"Conditions: {text_desc}")
    if wind_speed is not None:
        print(f"Wind Speed: {wind_speed:.1f} m/s")
    else:
        print("Wind Speed: Not available")


get_current_weather()