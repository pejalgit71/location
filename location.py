import streamlit as st
import json

st.set_page_config(page_title="📍 GPS Tracker + Map", page_icon="🗺️")
st.title("📍 GPS Tracker with Map")

# A placeholder to store coordinates
if "gps" not in st.session_state:
    st.session_state["gps"] = None

# A JS listener to receive messages from the iframe
st.markdown("""
<script>
window.addEventListener("message", (event) => {
    if (event.data.type === "gps_data") {
        const coords = event.data.value;
        // Update Streamlit input programmatically
        const input = document.querySelector('input[data-testid="stTextInput-input"]');
        if (input) {
            input.value = coords;
            input.dispatchEvent(new Event('input', { bubbles: true }));
        }
    }
});
</script>
""", unsafe_allow_html=True)

gps_html = """
<div style="max-width:600px; margin:auto;">
    <button onclick="getLocation()" style="width:100%; padding:10px; font-size:16px;">📍 Get My Location</button>
    <p id="output" style="text-align:center; margin-top:10px;">Waiting for location...</p>
    <div id="map" style="height:400px; width:100%; border:1px solid #ccc; border-radius:8px;"></div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
var map = L.map('map', {tap:false}).setView([0,0], 2);
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    tileSize: 256,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var marker;

function getLocation() {
    const output = document.getElementById('output');

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const lat = pos.coords.latitude.toFixed(6);
            const lon = pos.coords.longitude.toFixed(6);
            const acc = pos.coords.accuracy.toFixed(1);

            output.innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br>Accuracy: ±${acc} m`;

            map.setView([lat, lon], 16);
            if (marker) { map.removeLayer(marker); }
            marker = L.marker([lat, lon]).addTo(map);

            // SEND TO STREAMLIT VIA postMessage (works on iPhone!)
            window.parent.postMessage({
                type: "gps_data",
                value: lat + "," + lon + "," + acc
            }, "*");
        },
        (err) => {
            output.innerHTML = "Error: " + err.message;
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
}
</script>
"""

st.components.v1.html(gps_html, height=550)

# Text input that will be filled by JS
coords = st.text_input("gps_box", label_visibility="collapsed")

if coords:
    try:
        lat, lon, acc = map(float, coords.split(","))
        st.success(f"GPS Found: Accuracy ±{acc} m")
        st.write("Latitude:", lat)
        st.write("Longitude:", lon)
    except:
        st.error("Parsing error. Try again.")
else:
    st.info("Click the button above and allow location permission.")
