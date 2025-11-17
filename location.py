import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(page_title="GPS", page_icon="📍")
st.title("📍 GPS Tracker")

gps_html = """
<div style="max-width:600px; margin:auto;">
    <button onclick="getLocation()" style="width:100%; padding:10px; font-size:16px;">📍 Get My Location</button>
    <p id="output" style="text-align:center; margin-top:10px;">Waiting...</p>
    <div id="map" style="height:350px; width:100%; border:1px solid #ccc;"></div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
var map = L.map('map', {tap:false}).setView([0,0], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19
}).addTo(map);

var marker;

function getLocation() {
    if (!navigator.geolocation) {
        document.getElementById('output').innerHTML = "Geolocation not supported.";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const lat = pos.coords.latitude.toFixed(6);
            const lon = pos.coords.longitude.toFixed(6);
            const acc = pos.coords.accuracy.toFixed(1);

            // Update map
            map.setView([lat, lon], 16);
            if (marker) map.removeLayer(marker);
            marker = L.marker([lat, lon]).addTo(map);

            // Display
            document.getElementById('output').innerHTML =
                "Lat: " + lat + "<br>Lon: " + lon + "<br>Acc: ±" + acc + " m";

            // SEND RESULT TO STREAMLIT (OFFICIAL SUPPORTED METHOD)
            window.parent.postMessage(
                { "streamlitMessage": {"value": lat + "," + lon + "," + acc} },
                "*"
            );
        },
        (err) => {
            document.getElementById('output').innerHTML = "Error: " + err.message;
        },
        { enableHighAccuracy: true }
    );
}
</script>
"""

# Render component and capture returned data
result = components.html(gps_html, height=550)

# Streamlit receives GPS values HERE
coords = st.session_state.get("components", None)

if coords:
    try:
        lat, lon, acc = map(float, coords.split(","))
        st.success(f"GPS Found (±{acc} m)")
        st.write("Latitude:", lat)
        st.write("Longitude:", lon)
    except:
        st.error("Failed to parse GPS data.")
else:
    st.info("Click the button to get your location.")
