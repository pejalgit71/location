import streamlit as st

st.set_page_config(page_title="📍 GPS Tracker + Map", page_icon="🗺️")
st.title("📍 GPS Tracker with Map")
st.write("Click the button to get your location. The map will display your position without gaps.")

# HTML + JS
gps_html = """
<div style="max-width:600px; margin:auto;">
    <button onclick="getLocation()" style="width:100%; padding:10px; font-size:16px;">📍 Get My Location</button>
    <p id="output" style="text-align:center; margin-top:10px;">Waiting for location...</p>
    <div id="map" style="height:400px; width:100%; border:1px solid #ccc; border-radius:8px;"></div>
</div>

<link rel="stylesheet" href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css" />
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
var map = L.map('map', {tap:false}).setView([0,0], 2); // tap:false removes tile bugs
L.tileLayer('https://tile.openstreetmap.org/{z}/{x}/{y}.png', {
    maxZoom: 19,
    tileSize: 256,
    detectRetina: true,
    attribution: '&copy; OpenStreetMap contributors'
}).addTo(map);

var marker;

function getLocation() {
    const output = document.getElementById('output');
    if (!navigator.geolocation) {
        output.innerHTML = "Geolocation not supported.";
        return;
    }

    navigator.geolocation.getCurrentPosition(
        (pos) => {
            const lat = pos.coords.latitude.toFixed(6);
            const lon = pos.coords.longitude.toFixed(6);
            const acc = pos.coords.accuracy.toFixed(1);

            output.innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br>Accuracy: ±${acc} m`;

            // Update map
            map.setView([lat, lon], 16);
            if (marker) { map.removeLayer(marker); }
            marker = L.marker([lat, lon]).addTo(map)
                .bindPopup(`📍 You are here<br>Accuracy: ±${acc} m`)
                .openPopup();

            // Send to Streamlit textarea (inside iframe)
            const hidden_input = document.querySelector('textarea#gps_data');
            if (hidden_input) {
                hidden_input.value = lat + "," + lon + "," + acc;
                hidden_input.dispatchEvent(new Event('input', { bubbles: true }));
            }
        },
        (err) => {
            output.innerHTML = "Error: " + err.message;
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
}
</script>
"""

# Inject custom HTML
st.components.v1.html(gps_html, height=550)

# Hidden textarea for receiving GPS values
coords = st.text_area("Hidden GPS data", key="gps_data", label_visibility="collapsed")

# Process received GPS data
if coords:
    try:
        lat, lon, acc = map(float, coords.split(","))
        st.success(f"✅ Location Found! Accuracy ±{acc:.1f} m")
        st.write(f"**Latitude:** {lat}")
        st.write(f"**Longitude:** {lon}")
        st.markdown(f"[🌍 Open in Google Maps](https://www.google.com/maps?q={lat},{lon})")
    except:
        st.warning("⚠️ Could not parse GPS data. Try clicking the button again.")
else:
    st.info("Click the button above and allow location permission.")
