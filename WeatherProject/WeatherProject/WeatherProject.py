from tkinterweb import HtmlFrame
import threading
import webbrowser
import tkinter as tk
from tkinter import ttk
from geopy.geocoders import Nominatim
import requests
import json
from datetime import datetime
from PIL import Image, ImageTk
import io
from io import BytesIO
import traceback
from tkinter import messagebox
import ttkthemes
from matplotlib.figure import Figure
from matplotlib.backends.backend_tkagg import FigureCanvasTkAgg
import matplotlib.dates as mdates

geolocator = Nominatim(user_agent="(Logan Labinski, student, loganlabinski47@gmail.com)")

# Globals
root = None
entry = None
output_label = None
location = None
daily_forecast_table = None
hourly_forecast_table = None
notebook = None
radar_frame = None
open_radar_btn = None
graph_frame = None  # Add this line

# Keep references to icons so they aren’t garbage collected
icon_cache = {"daily": [], "hourly": []}

# Latest lat/lon (for radar button)
latest_lat = None
latest_lon = None

# Theme definitions
THEMES = {
    "Default": {
        "bg": "SystemButtonFace",
        "fg": "black",
        "select_bg": "#cfcfcf",
        "select_fg": "white",
        "tree_bg": "white",
        "tree_fg": "black"
    },
    "Dark": {
        "bg": "#2B2B2B",
        "fg": "#808080",
        "select_bg": "#6b6b6b",
        "select_fg": "white",
        "tree_bg": "#3C3F41",
        "tree_fg": "#FFFFFF"
    },
    "Light Blue": {
        "bg": "#E6F3FF",
        "fg": "black",
        "select_bg": "#0078D7",
        "select_fg": "white",
        "tree_bg": "white",
        "tree_fg": "black"
    },
    "Nature": {
        "bg": "#E8F5E9",
        "fg": "#1B5E20",
        "select_bg": "#2E7D32",
        "select_fg": "white",
        "tree_bg": "white",
        "tree_fg": "#1B5E20"
    }
}

def safe_json(response):
    try:
        return response.json()
    except Exception:
        content = response.content
        # Try response's declared encoding first if available
        if response.encoding:
            try:
                text = content.decode(response.encoding)
                return json.loads(text)
            except Exception:
                pass
        # Then try our fallback encodings
        for enc in ("utf-8", "utf-8-sig", "iso-8859-1", "latin-1", "cp1252"):
            try:
                text = content.decode(enc)
                return json.loads(text)
            except Exception:
                continue
        # Last resort: replace invalid characters
        text = content.decode("utf-8", errors="replace")
        return json.loads(text)


def format_time(iso_str):
    try:
        dt = datetime.fromisoformat(iso_str)
        return dt.strftime("%I %p").lstrip("0")
    except Exception:
        return iso_str


def download_icon_bytes(url, timeout=10):
    """Return raw bytes of icon or None on failure."""
    if not url:
        return None
    try:
        r = requests.get(url, timeout=timeout)
        r.raise_for_status()
        return r.content
    except Exception:
        return None


def apply_theme(theme_name):
    if theme_name not in THEMES:
        return

    theme = THEMES[theme_name]

    root.configure(bg=theme["bg"])

    style = ttk.Style()
    style.theme_use('default')  # Ensure the default theme is used

    # Custom tab style for Notebook
    style.configure("CustomNotebook.Tab",
                    background=theme["bg"],
                    foreground=theme["fg"],
                    padding=[10, 2],
                    font=('TkDefaultFont', 10, 'bold'))
    style.map("CustomNotebook.Tab",
              background=[("selected", theme["select_bg"]), ("active", theme["bg"])],
              foreground=[("selected", theme["select_fg"]), ("active", theme["fg"])])
    
    # Apply the custom tab style to the Notebook
    style.configure("TNotebook", background=theme["bg"], borderwidth=0)
    style.configure("TNotebook.Tab", background=theme["bg"], foreground=theme["fg"])
    style.map("TNotebook.Tab",
              background=[("selected", theme["select_bg"]), ("active", theme["bg"])],
              foreground=[("selected", theme["select_fg"]), ("active", theme["fg"])])
    
    # Frame backgrounds
    style.configure("TFrame", background=theme["bg"])

    # Treeview
    style.configure("Treeview",
                    background=theme["tree_bg"],
                    foreground=theme["tree_fg"],
                    fieldbackground=theme["tree_bg"])
    style.map("Treeview",
              background=[("selected", theme["select_bg"])],
              foreground=[("selected", theme["select_fg"])])
    
    style.configure("Treeview.Heading",
                    background=theme["bg"],
                    foreground=theme["fg"])

    # Update all direct children widgets
    for widget in root.winfo_children():
        if isinstance(widget, tk.Label):
            widget.configure(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, tk.Frame):
            widget.configure(bg=theme["bg"])
            for child in widget.winfo_children():
                if isinstance(child, tk.Label):
                    child.configure(bg=theme["bg"], fg=theme["fg"])
                elif isinstance(child, tk.Entry):
                    child.configure(bg=theme["tree_bg"], fg=theme["tree_fg"])
                elif isinstance(child, tk.Button):
                    child.configure(bg=theme["bg"], fg=theme["fg"])
        elif isinstance(widget, ttk.Notebook):
            widget.configure(style="TNotebook")
            for i in range(widget.index("end")):
                tab_frame = widget.nametowidget(widget.tabs()[i])
                tab_frame.configure(style="TFrame")
                for child in tab_frame.winfo_children():
                    if isinstance(child, tk.Label):
                        child.configure(bg=theme["bg"], fg=theme["fg"])
                    elif isinstance(child, tk.Button):
                        child.configure(bg=theme["bg"], fg=theme["fg"])

    root.current_theme = theme_name


def main():
    global root, entry, output_label, daily_forecast_table, hourly_forecast_table, notebook, radar_frame, open_radar_btn, graph_frame

    root = tk.Tk()
    root.title("Weather by Address")
    root.geometry("1000x700")
    
    # Add menubar
    menubar = tk.Menu(root)
    root.config(menu=menubar)
    
    # Add Themes menu
    themes_menu = tk.Menu(menubar, tearoff=0)
    menubar.add_cascade(label="Themes", menu=themes_menu)
    
    # Add theme options
    for theme_name in THEMES.keys():
        themes_menu.add_command(
            label=theme_name,
            command=lambda t=theme_name: apply_theme(t)
        )
    
    # Store current theme
    root.current_theme = "Default"

    label = tk.Label(root, text="Enter an address, city, or state within the United States:")
    label.pack(pady=5)

    entry = tk.Entry(root, width=60)
    entry.pack(pady=5)

    # Use a frame for the top row so we can add an "Enter" binding easily
    top_frame = tk.Frame(root)
    top_frame.pack(pady=2)
    # Move the entry into top_frame
    entry.pack_forget()
    entry = tk.Entry(top_frame, width=52)
    entry.pack(side="left", padx=(0, 6))
    # Button launches a worker thread so UI doesn't block
    button = tk.Button(top_frame, text="Get Weather", command=lambda: threading.Thread(target=fetch_and_update_weather, daemon=True).start())
    button.pack(side="left")

    # Allow pressing Enter to trigger the same
    entry.bind("<Return>", lambda e: threading.Thread(target=fetch_and_update_weather, daemon=True).start())

    output_label = tk.Label(root, text="", justify="center")
    output_label.pack(pady=8, fill="x", padx=6, anchor="center")

    notebook = ttk.Notebook(root, style="TNotebook")
    notebook.pack(pady=10, fill="both", expand=True)

    # Daily forecast tab
    daily_frame = ttk.Frame(notebook)
    notebook.add(daily_frame, text="Daily Forecast")

    daily_forecast_table = ttk.Treeview(
        daily_frame,
        columns=("Period", "Forecast", "Temp"),
        show="tree headings",
        height=10,
    )
    daily_forecast_table.heading("#0", text="Icon")
    daily_forecast_table.column("#0", width=50, anchor="center")
    daily_forecast_table.heading("Period", text="Period")
    daily_forecast_table.heading("Forecast", text="Forecast")
    daily_forecast_table.heading("Temp", text="Temp")
    daily_forecast_table.column("Period", width=120, anchor="w")
    daily_forecast_table.column("Forecast", width=500, anchor="w")
    daily_forecast_table.column("Temp", width=80, anchor="center")
    daily_forecast_table.pack(pady=10, fill="both", expand=True)

    # Hourly forecast tab
    hourly_frame = ttk.Frame(notebook)
    notebook.add(hourly_frame, text="Hourly Forecast")

    hourly_forecast_table = ttk.Treeview(
        hourly_frame,
        columns=("Time", "Forecast", "Temp"),
        show="tree headings",
        height=15,
    )
    hourly_forecast_table.heading("#0", text="Icon")
    hourly_forecast_table.column("#0", width=50, anchor="center")
    hourly_forecast_table.heading("Time", text="Time")
    hourly_forecast_table.heading("Forecast", text="Forecast")
    hourly_forecast_table.heading("Temp", text="Temp")
    hourly_forecast_table.column("Time", width=100, anchor="w")
    hourly_forecast_table.column("Forecast", width=500, anchor="w")
    hourly_forecast_table.column("Temp", width=80, anchor="center")
    hourly_forecast_table.pack(pady=10, fill="both", expand=True)

    # Radar map tab (non-blocking): open RainViewer in browser
    radar_frame = ttk.Frame(notebook)
    notebook.add(radar_frame, text="Radar Map")

    # Radar tab contents: short description + button to open interactive map in web browser
    radar_desc = tk.Label(radar_frame, text="Interactive radar is opened in your web browser. Center it on the current location using the button below.", wraplength=800, justify="left")
    radar_desc.pack(pady=(12, 6), padx=10)

    open_radar_btn = tk.Button(radar_frame, text="Open Interactive Radar in Browser", state="disabled", command=lambda: open_rainviewer(lat=latest_lat, lon=latest_lon))
    open_radar_btn.pack(pady=6)

    # Temperature Graph tab
    graph_frame = ttk.Frame(notebook)
    notebook.add(graph_frame, text="Temperature Graph")

    # Small helper: open RainViewer for the given lat/lon
    def open_rainviewer(lat=None, lon=None):
        if not lat or not lon:
            tk.messagebox.showinfo("No location", "Please fetch weather for an address first.")
            return
        url = f"https://www.rainviewer.com/map.html?loc={lat},{lon},7&oFa=1&oC=1&oU=1&oMC=1&rmt=1&c=1&sm=1&sn=1"
        webbrowser.open_new_tab(url)

    # Keep a reference to the helper in globals for the button's lambda closure
    # (we'll update the button's command by replacing the lambda above when new location arrives)
    
    # Apply default theme at startup
    apply_theme("Default")
    
    root.mainloop()


def fetch_and_update_weather():
    """
    Worker thread: performs geocoding and NWS network calls and downloads icon bytes.
    Posts results back to the main thread using root.after(...)
    """
    global latest_lat, latest_lon

    # Show loading message immediately
    root.after(0, lambda: output_label.config(text="Loading..."))

    address = entry.get().strip()
    if not address:
        root.after(0, lambda: output_label.config(text="Please enter an address."))
        return

    try:
        # Geocode (this is blocking — but in worker thread that's okay)
        loc = geolocator.geocode(address, timeout=10)
    except Exception as e:
        err = f"Geocoding error: {e}"
        root.after(0, lambda: output_label.config(text=err))
        return

    if not loc:
        root.after(0, lambda: output_label.config(text="Address not found."))
        return

    lat = loc.latitude
    lon = loc.longitude
    latest_lat, latest_lon = lat, lon

    headers = {"User-Agent": "Logan Labinski (loganlabinski47@gmail.com)"}

    try:
        # single /points call
        points_url = f"https://api.weather.gov/points/{lat},{lon}"
        points_response = requests.get(points_url, headers=headers, timeout=15)
        points_data = safe_json(points_response)

        # Stations -> station id -> latest obs
        stations_url = points_data["properties"]["observationStations"]
        stations_response = requests.get(stations_url, headers=headers, timeout=15)
        stations_data = safe_json(stations_response)
        station_id = stations_data["features"][0]["properties"]["stationIdentifier"]

        latest_obs_url = f"https://api.weather.gov/stations/{station_id}/observations/latest"
        obs_response = requests.get(latest_obs_url, headers=headers, timeout=15)
        obs_data = safe_json(obs_response)

        # forecast (daily) and hourly
        forecast_url = points_data["properties"].get("forecast")
        if forecast_url:
            forecast_response = requests.get(forecast_url, headers=headers, timeout=15)
            forecast_data = safe_json(forecast_response)
            periods = forecast_data.get("properties", {}).get("periods", [])
        else:
            periods = []

        forecast_hourly_url = points_data["properties"].get("forecastHourly")
        if forecast_hourly_url:
            hourly_response = requests.get(forecast_hourly_url, headers=headers, timeout=15)
            hourly_data = safe_json(hourly_response)
            hourly_periods = hourly_data.get("properties", {}).get("periods", [])
        else:
            hourly_periods = []

        # Download icon bytes for each period (so we can create PhotoImage on main thread)
        daily_icon_bytes = []
        for p in periods:
            icon_url = p.get("icon")
            daily_icon_bytes.append(download_icon_bytes(icon_url))

        hourly_icon_bytes = []
        for p in hourly_periods[:24]:
            icon_url = p.get("icon")
            hourly_icon_bytes.append(download_icon_bytes(icon_url))

        # --- NEW: Fetch alerts ---
        alerts_url = f"https://api.weather.gov/alerts/active?point={lat},{lon}"
        alerts_response = requests.get(alerts_url, headers=headers, timeout=15)
        alerts_data = safe_json(alerts_response)
        alerts = alerts_data.get("features", [])
        alert_messages = []
        for alert in alerts:
            headline = alert.get("properties", {}).get("headline")
            if headline:
                alert_messages.append(headline)
    except Exception as e:
        tb = traceback.format_exc()
        root.after(0, lambda: output_label.config(text=f"Network/API error: {e}\n{tb.splitlines()[-1]}"))
        return

    # Build current conditions text (done here so worker thread doesn't need to touch UI)
    try:
        props = obs_data.get("properties", {})

        temp_c = props.get("temperature", {}).get("value")
        temp_f = temp_c * 9 / 5 + 32 if temp_c is not None else None
        text_desc = props.get("textDescription", "N/A")

        humidity = props.get("relativeHumidity", {}).get("value")
        pressure = props.get("barometricPressure", {}).get("value")
        visibility = props.get("visibility", {}).get("value")
        
        # Add wind speed data
        wind_speed = props.get("windSpeed", {}).get("value")
        wind_direction = props.get("windDirection", {}).get("value")
        
        feels_like_c = props.get("heatIndex", {}).get("value") or props.get("windChill", {}).get("value")
        feels_like_f = feels_like_c * 9 / 5 + 32 if feels_like_c is not None else None

        text_lines = [f"Current conditions at {station_id}:"]
        if temp_f is not None:
            text_lines.append(f"Temperature: {temp_f:.1f}\N{DEGREE SIGN}F")
        else:
            text_lines.append("Temperature: Not available")
        if feels_like_f is not None:
            text_lines.append(f"Feels Like: {feels_like_f:.1f}\N{DEGREE SIGN}F")

        text_lines.append(f"Conditions: {text_desc}")

        # Add wind information
        if wind_speed is not None:
            try:
                wind_speed_mph = wind_speed * 2.237  # Convert m/s to mph
                direction_text = ""
                if wind_direction is not None:
                    direction_text = f" from {wind_direction}\N{DEGREE SIGN}"
                text_lines.append(f"Wind: {wind_speed_mph:.1f} mph{direction_text}")
            except Exception:
                text_lines.append(f"Wind: {wind_speed}")

        if humidity is not None:
            try:
                text_lines.append(f"Humidity: {humidity:.0f}%")
            except Exception:
                text_lines.append(f"Humidity: {humidity}")
        if pressure is not None:
            try:
                text_lines.append(f"Pressure: {pressure/100:.1f} hPa")
            except Exception:
                text_lines.append(f"Pressure: {pressure}")
        if visibility is not None:
            try:
                text_lines.append(f"Visibility: {visibility/1000:.1f} km")
            except Exception:
                text_lines.append(f"Visibility: {visibility}")

        # --- NEW: Add alerts to output ---
        if alert_messages:
            text_lines.append("\n⚠ Extreme Weather Alerts:")
            for msg in alert_messages:
                text_lines.append(f"- {msg}")

        current_text = "\n".join(text_lines)
    except Exception as e:
        current_text = f"Error building current conditions: {e}"

    # Now post updates to the main thread to update UI (create PhotoImage objects there)
    root.after(0, lambda: update_ui_with_fetched(current_text, periods, hourly_periods, daily_icon_bytes, hourly_icon_bytes, lat, lon))


def update_ui_with_fetched(current_text, periods, hourly_periods, daily_icon_bytes, hourly_icon_bytes, lat, lon):
    """
    Run in main Tk thread: update labels and Treeviews, create PhotoImage objects from bytes.
    """
    global icon_cache, latest_lat, latest_lon, open_radar_btn

    latest_lat, latest_lon = lat, lon

    # Update current conditions label
    output_label.config(text=current_text)

    # ------- Daily -------
    for row in daily_forecast_table.get_children():
        daily_forecast_table.delete(row)
    icon_cache["daily"].clear()

    for idx, p in enumerate(periods):
        period_name = p.get("name", "")
        short_forecast = p.get("shortForecast", "")
        temp = f"{p.get('temperature', '')}\N{DEGREE SIGN}{p.get('temperatureUnit', '')}"
        
        # Add precipitation probability if available
        prob_precip = p.get("probabilityOfPrecipitation", {}).get("value")
        if prob_precip is not None and prob_precip > 0:
            short_forecast = f"{short_forecast} ({prob_precip}% chance of precipitation)"

        img_bytes = daily_icon_bytes[idx] if idx < len(daily_icon_bytes) else None
        photo = None
        if img_bytes:
            try:
                pil_im = Image.open(BytesIO(img_bytes)).convert("RGBA")
                pil_im = pil_im.resize((32, 32), Image.LANCZOS)
                photo = ImageTk.PhotoImage(pil_im)
            except Exception:
                photo = None
        icon_cache["daily"].append(photo)
        # Insert with image into #0 (tree) column
        daily_forecast_table.insert("", "end", text="", image=photo, values=(period_name, short_forecast, temp))

    # ------- Hourly -------
    for row in hourly_forecast_table.get_children():
        hourly_forecast_table.delete(row)
    icon_cache["hourly"].clear()

    for idx, p in enumerate(hourly_periods[:24]):
        display_time = format_time(p.get("startTime", ""))
        short_forecast = p.get("shortForecast", "")
        temp = f"{p.get('temperature', '')}\N{DEGREE SIGN}{p.get('temperatureUnit', '')}"

        # Add precipitation probability if available
        prob_precip = p.get("probabilityOfPrecipitation", {}).get("value")
        if prob_precip is not None and prob_precip > 0:
            short_forecast = f"{short_forecast} ({prob_precip}% chance of precipitation)"

        img_bytes = hourly_icon_bytes[idx] if idx < len(hourly_icon_bytes) else None
        photo = None
        if img_bytes:
            try:
                pil_im = Image.open(BytesIO(img_bytes)).convert("RGBA")
                pil_im = pil_im.resize((32, 32), Image.LANCZOS)
                photo = ImageTk.PhotoImage(pil_im)
            except Exception:
                photo = None
        icon_cache["hourly"].append(photo)
        hourly_forecast_table.insert("", "end", text="", image=photo, values=(display_time, short_forecast, temp))

    # ------- Enable radar button now that we have lat/lon -------
    try:
        if open_radar_btn:
            # Reconfigure the button to have a working command bound to the current lat/lon
            open_radar_btn.config(state="normal", command=lambda lat=lat, lon=lon: webbrowser.open_new_tab(f"https://www.rainviewer.com/map.html?loc={lat},{lon},7&oFa=1&oC=1&oU=1&oMC=1&rmt=1&c=1&sm=1&sn=1"))
    except Exception:
        pass

    # ------- Update temperature graph -------
    update_temperature_graph(graph_frame, hourly_periods)


def update_temperature_graph(frame, hourly_data):
    """Create/update temperature graph in the given frame"""
    # Clear existing graph if any
    for widget in frame.winfo_children():
        widget.destroy()
    
    # Extract time and temperature data
    times = []
    temps = []
    for period in hourly_data[:24]:  # Next 24 hours
        time = datetime.fromisoformat(period.get('startTime', ''))
        temp = period.get('temperature')
        if temp is not None:
            times.append(time)
            temps.append(temp)
    
    # Create the figure and plot
    fig = Figure(figsize=(10, 4), dpi=100)
    ax = fig.add_subplot(111)
    
    # Plot temperature line
    ax.plot(times, temps, '-o', color='#0078D7', linewidth=2, markersize=4)
    
    # Customize the plot
    ax.set_title('24-Hour Temperature Forecast')
    ax.set_xlabel('Time')
    ax.set_ylabel('Temperature (°F)')
    
    # Format x-axis to show hours
    ax.xaxis.set_major_formatter(mdates.DateFormatter('%I %p'))
    fig.autofmt_xdate()  # Rotate and align the tick labels
    
    # Add grid
    ax.grid(True, linestyle='--', alpha=0.7)
    
    # Adjust layout
    fig.tight_layout()
    
    # Create canvas and add to frame
    canvas = FigureCanvasTkAgg(fig, master=frame)
    canvas.draw()
    canvas.get_tk_widget().pack(fill='both', expand=True, padx=10, pady=10)


if __name__ == "__main__":
    main()