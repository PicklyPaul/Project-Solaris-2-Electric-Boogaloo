import webview
import requests
from final import compute
# -------------------------
# UI
# -------------------------

ui = '''<!DOCTYPE html>
<html lang="en">
<head>
<meta charset="UTF-8">
<meta name="viewport" content="width=device-width, initial-scale=1.0">
<title>Solaris – Weather Odds</title>

<style>
:root {
    --bg-main: #d0e8ff;       /* Sky blue background */
    --bg-panel: #ffffff;       /* White panels */
    --accent: #ffae42;         /* Sunny orange accent */
    --accent-soft: #ffdf7f;    /* Soft sunny highlight */
    --card-bg: #f0f8ff;        /* Light card background */
    --text-main: #0b3d91;      /* Deep blue text */
    --text-muted: #4d6fa6;     /* Muted blue text */
}

* { box-sizing: border-box; }

body {
    margin: 0;
    font-family: "Segoe UI", Roboto, sans-serif;
    background: linear-gradient(to bottom, #a0d8ff, #d0e8ff);
    color: var(--text-main);
}

header {
    text-align: center;
    padding: 1.5rem 1rem;
    background: linear-gradient(180deg, #67cfff, #36a9ff);
    border-bottom: 3px solid var(--accent);
}

header h1 {
    margin: 0;
    color: var(--accent);
    font-size: 2.2rem;
}

header p {
    margin-top: 0.3rem;
    color: var(--text-muted);
    font-size: 1rem;
}

main {
    max-width: 1200px;
    margin: auto;
    padding: 1.5rem;
    display: flex;
    flex-direction: column;
    gap: 1.5rem;
    align-items: center;
}

/* INPUT PANEL */
#input-panel {
    background: var(--bg-panel);
    padding: 1rem;
    border-radius: 16px;
    width: 80%;
    box-shadow: 0 8px 20px rgba(100,150,200,0.3);
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

#input-panel h2 {
    margin-top: 0;
    color: var(--accent);
}

form {
    display: flex;
    flex-direction: column;
    gap: 0.8rem;
}

label {
    font-size: 0.85rem;
    color: var(--text-muted);
}

input {
    padding: 0.6rem;
    border-radius: 6px;
    border: 1px solid #bcdfff;
    font-size: 0.95rem;
}

button {
    margin-top: 0.5rem;
    padding: 0.8rem;
    background: var(--accent);
    color: white;
    font-size: 0.95rem;
    font-weight: bold;
    border: none;
    border-radius: 8px;
    cursor: pointer;
    transition: transform 0.2s, background 0.3s;
}

button:hover {
    background: #e69530;
    transform: translateY(-1px);
}

/* MAP PANEL */
#map-panel {
    width: 80%;
    height: 400px; /* reduced height */
    border-radius: 14px;
    overflow: hidden;
    box-shadow: 0 8px 25px rgba(100,150,200,0.4);
}

#map-container {
    width: 100%;
    height: 100%;
}

/* WEATHER DASHBOARD */
#weather-dashboard {
    background: var(--bg-panel);
    padding: 1.5rem;
    border-radius: 16px;
    width: 80%;
    box-shadow: 0 8px 25px rgba(100,150,200,0.3);
}

#weather-dashboard h2 {
    margin-top: 0;
    color: var(--accent);
    margin-bottom: 1rem;
}

.weather-grid {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(180px, 1fr));
    gap: 1rem;
}

.weather-card {
    background: var(--card-bg);
    padding: 0.9rem;
    border-radius: 12px;
    box-shadow: inset 0 0 0 1px rgba(150,200,255,0.2);
}

.weather-card h3 {
    margin: 0;
    font-size: 0.85rem;
    color: var(--text-muted);
}

.weather-value {
    margin-top: 0.3rem;
    font-size: 1.4rem;
    font-weight: bold;
    color: var(--accent-soft);
}

.weather-unit {
    font-size: 0.75rem;
    color: var(--text-muted);
    margin-left: 4px;
}

footer {
    text-align: center;
    padding: 1.2rem;
    color: var(--text-muted);
    border-top: 1px solid rgba(0,0,0,0.1);
    margin-top: 1.5rem;
}

@media (max-width: 1200px) {
    #input-panel,
    #map-panel,
    #weather-dashboard {
        width: 92%;
    }

    #map-panel {
        height: 360px;
    }
}

/* Small screens (tablets & small laptops) */
@media (max-width: 900px) {
    header h1 {
        font-size: 2rem;
    }

    main {
        padding: 1rem;
        gap: 1.2rem;
    }

    #map-panel {
        height: 320px;
    }

    .weather-grid {
        grid-template-columns: repeat(auto-fit, minmax(160px, 1fr));
    }
}

/* Mobile / very small windows */
@media (max-width: 600px) {
    header {
        padding: 1rem;
    }

    header h1 {
        font-size: 1.7rem;
    }

    header p {
        font-size: 0.9rem;
    }

    #input-panel,
    #map-panel,
    #weather-dashboard {
        width: 100%;
    }

    #map-panel {
        height: 280px;
    }

    input,
    button {
        font-size: 0.9rem;
        padding: 0.6rem;
    }

    .weather-value {
        font-size: 1.2rem;
    }
}

/* =========================
   SKY BACKGROUND ANIMATION
   ========================= */

.sky-background {
    position: fixed;
    inset: 0;
    z-index: -1;
    overflow: hidden;
    background: linear-gradient(to bottom, #9fdcff, #d0e8ff);
}

/* Sun */
.sun {
    position: absolute;
    top: 60px;
    right: 120px;
    width: 140px;
    height: 140px;
    background: radial-gradient(circle, #fff4b0 0%, #ffd25a 55%, rgba(255,210,90,0.4) 70%);
    border-radius: 50%;
    filter: blur(2px);
    animation: sunGlow 6s ease-in-out infinite alternate;
}

@keyframes sunGlow {
    from { transform: scale(1); opacity: 0.9; }
    to   { transform: scale(1.05); opacity: 1; }
}

/* Clouds */
.cloud {
    position: absolute;
    top: 15%;
    width: 220px;
    height: 70px;
    background: rgba(255,255,255,0.7);
    border-radius: 50px;
    filter: blur(1px);
}

.cloud::before,
.cloud::after {
    content: "";
    position: absolute;
    background: rgba(255,255,255,0.7);
    width: 90px;
    height: 90px;
    top: -45px;
    border-radius: 50%;
}

.cloud::before { left: 30px; }
.cloud::after  { right: 30px; }

/* Individual cloud motion */
.cloud-1 {
    top: 18%;
    left: -250px;
    animation: cloudMove 90s linear infinite;
}

.cloud-2 {
    top: 35%;
    left: -300px;
    opacity: 0.6;
    animation: cloudMove 120s linear infinite;
}

.cloud-3 {
    top: 55%;
    left: -350px;
    opacity: 0.5;
    animation: cloudMove 150s linear infinite;
}

@keyframes cloudMove {
    from { transform: translateX(0); }
    to   { transform: translateX(160vw); }
}


</style>


<!-- Leaflet.js -->
<link rel="stylesheet" href="https://unpkg.com/leaflet/dist/leaflet.css"/>
<script src="https://unpkg.com/leaflet/dist/leaflet.js"></script>

</head>
<body>
<div class="sky-background">
    <div class="sun"></div>
    <div class="cloud cloud-1"></div>
    <div class="cloud cloud-2"></div>
    <div class="cloud cloud-3"></div>
</div>
<header>
    <h1>Solaris 2.0</h1>
    <p>NASA Earth data to estimate future weather odds</p>
</header>

<main>

<!-- INPUT PANEL -->
<section id="input-panel">
    <h2>Location & Date</h2>

    <form id="Weatherform">
        <label>Address</label>
        <input id="address" type="text" placeholder="1234 Flower Ln, City, State">

        <label>Date</label>
        <input id="date" type="date" required>

        <button type="submit">Analyze Weather Odds</button>
    </form>
</section>

<!-- MAP PANEL -->
<section id="map-panel">
    <div id="map-container"></div>
</section>

<!-- WEATHER DASHBOARD -->
<section id="weather-dashboard">
    <h2>Weather Conditions</h2>
    <div class="weather-grid">
        <div class="weather-card">
            <h3>Temperature</h3>
            <div class="weather-value" id="temp">-- <span class="weather-unit">°C</span> </div>
        </div>

        <div class="weather-card">
            <h3>Humidty</h3>
            <div class="weather-value" id="hum">-- <span class="weather-unit">°C</span></div>
        </div>

        <div class="weather-card">
            <h3>Chance of Rain</h3>
            <div class="weather-value" id="rain">-- <span class="weather-unit">%</span></div>
        </div>

        <div class="weather-card">
            <h3>Snow Chance</h3>
            <div class="weather-value" id="snow">-- <span class="weather-unit">%</span></div>
        </div>

        <div class="weather-card">
            <h3>Wind Speed</h3>
            <div class="weather-value" id="wind">-- <span class="weather-unit">m/s</span></div>
        </div>

        <div class="weather-card">
            <h3>Air Quality Index</h3>
            <div class="weather-value" id="aqi">--</div>
        </div>
    </div>
</section>

</main>

<footer>
    Solaris · NASA Space Apps Challenge 2025 · Earth Observation Data
</footer>

<script>
function update_dash(data) {
    if (!data) return;

    // 1. Update Temperature
    document.getElementById("temp").innerHTML = 
        `${data.temp.toFixed(1)} <span class="weather-unit">°C</span>`;

    // 2. Update  humidity
    document.getElementById("hum").innerHTML = 
        `${data.hum.toFixed(1)} <span class="weather-unit">%</span>`;

    // 3. Update Chance of Rain
    document.getElementById("rain").innerHTML = 
        `${data.rain.toFixed(0)} <span class="weather-unit">%</span>`;

    // 4. Update Snow Chance
    document.getElementById("snow").innerHTML = 
        `${data.snow.toFixed(0)} <span class="weather-unit">%</span>`;

    // 5. Update Wind Speed
    document.getElementById("wind").innerHTML = 
        `${data.wind.toFixed(1)} <span class="weather-unit">m/s</span>`;
    }
window.addEventListener("pywebviewready", () => {

    // Handle form submit
    const form = document.getElementById("Weatherform");
    form.addEventListener("submit", (e) => {
        e.preventDefault();

        const payload = {
            address: document.getElementById("address").value,
            date: document.getElementById("date").value
        };

        window.pywebview.api.receiveData(payload).then(weather_data => {
            update_dash(weather_data);
        });
    });

    // Initialize map
    const map = L.map('map-container').setView([20, 0], 2);
    L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
        maxZoom: 19,
    }).addTo(map);

    let pin;

    // Pin-drop functionality
    map.on('click', function(e) {
        const lat = e.latlng.lat;
        const lon = e.latlng.lng;

        if (pin) { map.removeLayer(pin); }

        pin = L.marker([lat, lon]).addTo(map);

        // Send coordinates to Python
        window.pywebview.api.receiveData({
            address: null,
            date: document.getElementById("date").value,
            lat: lat,
            lon: lon
        }).then(resp => {
            console.log("Coordinates sent to backend:", resp);
        });
    });
    
    
});
</script>

</body>
</html>
'''

# -------------------------
# Global storage
# -------------------------
userInput = {}

# -------------------------
# Getting user input from JS
# -------------------------
class Api:
    def __init__(self):
        pass

    def receiveData(self, data):
        global userInput

        # Store user input
        stuff = {
            "lat": "",
            "lon": "",
            "date": ""
        }
        print("User input received:", data)

        # Extract fields safely
        address = data.get('address')
        date = data.get('date')

        print("Address:", address)
        print("Date:", date)

        # If lat/lon already provided (map pin)
        if data.get("lat") is not None and data.get("lon") is not None:
            lat = data["lat"]
            long = data["lon"]
            print("Coordinates from map:", lat, long)

        # Otherwise geocode the address
        elif address:
            lat, long = geocode(address)
            print("Coordinates from address:", lat, long)

        else:
            print("No location data provided")

        stuff['date'] = date
        stuff["lat"] = lat
        stuff["lon"] = long

        userInput = stuff
        print(userInput)
        try:
            lat = userInput["lat"]
            long = userInput["lon"]
            date = userInput["date"]
        except KeyError:
            print("No address/date inputed")
        # -------------------------
        # Data From Paul
        # -------------------------
        date = date.split("-")
        month = date[1]
        dist =  int(date[0]) - 2024
        result = compute(month, lat, long, dist)
        weather_data = {
            "temp":(result[0]- 272),
            "hum":result[1],
            "rain": result[2],
            "snow":result[3],
            "wind":result[4],
        #    "aqi":result[5] : requires aqi
        }
        return weather_data
        


# -------------------------
# Geocoding
# -------------------------
def geocode(address):
    url = "https://nominatim.openstreetmap.org/search"
    params = {
        "q": address,
        "format": "json",
        "limit": 1
    }
    headers = {
        "User-Agent": "Solaris-UserReq"
    }

    response = requests.get(url, params=params, headers=headers, timeout=10)
    response.raise_for_status()

    data = response.json()
    if not data:
        return None, None

    return float(data[0]['lat']), float(data[0]['lon'])


# -------------------------
# Displaying data
# -------------------------



# -------------------------
# Launching App
# -------------------------
api = Api()
window = webview.create_window(
    "NSAr",
    html=ui,
    js_api=api
)



webview.start()



