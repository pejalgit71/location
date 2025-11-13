import streamlit as st
from streamlit_folium import st_folium
import folium

st.set_page_config(page_title="📍 GPS Map Tracker", page_icon="🗺️")

st.title("📍 My GPS Location Map")
st.write("Tap the button below to detect your current location and view it on the map.")

# JavaScript to get location and send to Streamlit
gps_js = """
<button onclick="getLocation()">📍 Get My Location</button>
<p id="output">Waiting for location...</p>
<script>
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
            const coords = lat + "," + lon + "," + acc;
            const input = window.parent.document.querySelector('textarea[data-testid="stTextArea-input"]');
            const event = new Event('input', { bubbles: true });
            input.value = coords;
            input.dispatchEvent(event);
        },
        (err) => {
            output.innerHTML = "Error: " + err.message;
        },
        { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
    );
}
</script>
"""

# Inject HTML/JS
st.components.v1.html(gps_js, height=150)

# Hidden Streamlit field to receive location
coords = st.text_area("Location data", label_visibility="collapsed")

if coords:
    try:
        lat, lon, acc = map(float, coords.split(","))
        st.success(f"✅ Location found! (±{acc:.1f} m accuracy)")
        st.write(f"**Latitude:** {lat}  |  **Longitude:** {lon}")

        # Create Folium map
        map_center = [lat, lon]
        m = folium.Map(location=map_center, zoom_start=16)
        folium.Marker(
            map_center,
            popup=f"📍 You are here<br>Lat: {lat}<br>Lon: {lon}<br>Accuracy: ±{acc:.1f} m",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

        # Show map in Streamlit
        st_folium(m, width=700, height=500)
        st.markdown(f"[🌍 Open in Google Maps](https://www.google.com/maps?q={lat},{lon})")

    except Exception as e:
        st.warning("⚠️ Could not read location data. Try again.")
else:
    st.info("Click the button and allow GPS permission.")
