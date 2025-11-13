import streamlit as st

st.set_page_config(page_title="📍 GPS Tracker + Map", page_icon="🗺️")
st.title("📍 GPS Tracker with Map")
st.write("Click the button below to get your GPS coordinates and display them on a clean map frame.")

# HTML + JS block with responsive map
gps_html = """
<div style="max-width:600px; margin:auto;">
    <button onclick="getLocation()" style="width:100%; padding:10px; font-size:16px;">📍 Get My Location</button>
    <p id="output" style="text-align:center; margin-top:10px;">Waiting for location...</p>
    <div id="map" style="height:400px; width:100%; margin-top:10px; border:1px solid #ccc; border-radius:8px;"></div>
</div>

<link
  rel="stylesheet"
  href="https://unpkg.com/leaflet@1.9.4/dist/leaflet.css"
  integrity="sha256-sA+td4N6wNKfCMR4U5lHuVFV5RzhwKkxDRw8r0kPwwo="
  crossorigin=""
/>
<script src="https://unpkg.com/leaflet@1.9.4/dist/leaflet.js"></script>

<script>
var map = L.map('map').setView([0,0], 2);
L.tileLayer('https://{s}.tile.openstreetmap.org/{z}/{x}/{y}.png', {
  maxZoom: 19
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
                .bindPopup(`📍 You are here<br>Accuracy ±${acc} m`)
                .openPopup();

            // Send to Streamlit hidden textarea
            const hidden_input = window.parent.document.querySelector('textarea[data-testid="stTextArea-input"]');
            const event = new Event('input', { bubbles: true });
            hidden_input.value = lat + "," + lon + "," + acc;
            hidden_input.dispatchEvent(event);
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

# Hidden textarea to receive coordinates
coords = st.text_area("Hidden GPS data", label_visibility="collapsed")

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
