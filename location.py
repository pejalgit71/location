import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("📍 GPS Tracker – High-Detail Map (Leaflet)")

# --- 1. Get GPS from browser ---
location = streamlit_js_eval(
    js_expressions="""
        new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                pos => resolve({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    acc: pos.coords.accuracy
                }),
                err => resolve(null),
                { enableHighAccuracy: true }
            );
        });
    """,
    key="gps",
)

# --- 2. If GPS found ---
if location:
    st.success("GPS Received! 🎉")

    lat = location["lat"]
    lon = location["lon"]
    acc = location["acc"]

    st.write("**Latitude:**", lat)
    st.write("**Longitude:**", lon)
    st.write("**Accuracy:**", acc, "meters")

    # --- 3. Insert Leaflet map with CARTO Voyager ---
    leaflet_map = f"""
    <div id="map" style="height: 450px; width: 100%; border-radius: 10px;"></div>

    <link rel="stylesheet" href="https://unpkg.com/leaflet@1.7.1/dist/leaflet.css" />
    <script src="https://unpkg.com/leaflet@1.7.1/dist/leaflet.js"></script>

    <script>
        var map = L.map('map').setView([{lat}, {lon}], 16);

        // ⭐ Modern High-Detail Map – CARTO Voyager
        L.tileLayer('https://{{s}}.basemaps.cartocdn.com/rastertiles/voyager/{{z}}/{{x}}/{{y}}{{r}}.png', {{
            maxZoom: 19,
            attribution: '&copy; OpenStreetMap & CartoDB'
        }}).addTo(map);

        // Marker at GPS location
        L.marker([{lat}, {lon}]).addTo(map)
            .bindPopup("📍 You are here<br>Accuracy: ±{acc} m")
            .openPopup();
    </script>
    """

    st.components.v1.html(leaflet_map, height=470)

else:
    st.info("Click **Allow** when your browser asks for GPS location.")
