import tkinter as tk
from tkinter import ttk
from urllib import request
from geopy.geocoders import Nominatim
import requests

geolocator = Nominatim(user_agent="(Logan Labinski, student, loganlabinski47@gmail.com)")

# make these available to handlers
entry = None
output_label = None
location = None
forecast_table = None


def main():
    global entry, output_label, forecast_table
    root = tk.Tk()
    root.title("Weather by Address")
    root.geometry("700x500")

    # Label
    label = tk.Label(root, text="Enter an address:")
    label.pack(pady=5)

    # Text entry box
    entry = tk.Entry(root, width=50)
    entry.pack(pady=5)

    # Output label
    output_label = tk.Label(root, text="", justify="left")
    output_label.pack(pady=10)

    # Button
    button = tk.Button(root, text="Get Weather", command=show_weather)
    button.pack(pady=5)

    # Forecast Table
    forecast_table = ttk.Treeview(root, columns=("Period", "Forecast", "Temp"), show="headings", height=10)
    forecast_table.heading("Period", text="Period")
    forecast_table.heading("Forecast", text="Forecast")
    forecast_table.heading("Temp", text="Temp")
    forecast_table.column("Period", width=120, anchor="w")
    forecast_table.column("Forecast", width=400, anchor="w")
    forecast_table.column("Temp", width=80, anchor="center")
    forecast_table.pack(pady=10, fill="both", expand=True)

    # Instruction Label
    label2 = tk.Label(root, text="Type a new input and push button again to receive different data")
    label2.pack(pady=5)

    root.mainloop()


def show_weather():
    global location
    address = entry.get()
    if not address:
        output_label.config(text="Please enter an address.")
        return

    location = geolocator.geocode(address)
    if not location:
        output_label.config(text="Address not found.")
        return

    get_current_weather()
    get_forecast()


def get_current_weather():
    headers = {"User-Agent": "Logan Labinski (loganlabinski47@gmail.com)"}
    lat = location.latitude
    lon = location.longitude

    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    points_response = requests.get(points_url, headers=headers)
    points_data = points_response.json()

    stations_url = points_data["properties"]["observationStations"]
    stations_response = requests.get(stations_url, headers=headers)
    stations_data = stations_response.json()

    station_id = stations_data["features"][0]["properties"]["stationIdentifier"]

    latest_obs_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
    obs_response = requests.get(latest_obs_url, headers=headers)
    obs_data = obs_response.json()

    props = obs_data["properties"]
    temp_c = props["temperature"]["value"]
    temp_f = temp_c * 9/5 + 32 if temp_c is not None else None
    wind_speed = props["windSpeed"]["value"]
    text_desc = props["textDescription"]

    text = f"\nCurrent conditions at {station_id}:\n"
    text += f"Temperature: {temp_f:.1f}\N{DEGREE SIGN}F\n" if temp_f is not None else "Temperature: Not available\n"
    text += f"Conditions: {text_desc}\n"
    text += f"Wind Speed: {wind_speed:.1f} m/s\n" if wind_speed is not None else "Wind Speed: Not available\n"

    print(text)
    if output_label:
        output_label.config(text=text)


def get_forecast():
    headers = {"User-Agent": "Logan Labinski (loganlabinski47@gmail.com)"}
    lat = location.latitude
    lon = location.longitude

    points_url = f"https://api.weather.gov/points/{lat},{lon}"
    points_response = requests.get(points_url, headers=headers)
    points_data = points_response.json()

    forecast_url = points_data["properties"]["forecast"]
    forecast_response = requests.get(forecast_url, headers=headers)
    forecast_data = forecast_response.json()

    periods = forecast_data["properties"]["periods"]

    # Clear old rows
    for row in forecast_table.get_children():
        forecast_table.delete(row)

    # Insert new forecast data
    for p in periods:
        period_name = p["name"]
        short_forecast = p["shortForecast"]
        temp = f"{p['temperature']}\N{DEGREE SIGN}{p['temperatureUnit']}"
        forecast_table.insert("", "end", values=(period_name, short_forecast, temp))


if __name__ == "__main__":
    main()

