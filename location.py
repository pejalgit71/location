import streamlit as st
import json

st.set_page_config(page_title="📍 GPS Tracker", page_icon="🌍")

st.markdown(
    """
    <script>
    // Register PWA service worker
    if ('serviceWorker' in navigator) {
        navigator.serviceWorker.register('/static/service-worker.js');
    }
    </script>
    """,
    unsafe_allow_html=True
)

st.title("📍 My GPS Tracker (PWA Ready)")
st.write("Tap the button below to get your current location.")

# JavaScript to request location
html_code = """
<button onclick="getLocation()">📍 Get My Location</button>
<p id="output"></p>
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
      output.innerHTML = `Latitude: ${lat}<br>Longitude: ${lon}<br>Accuracy: ±${acc} m<br><a href="https://www.google.com/maps?q=${lat},${lon}" target="_blank">Open in Google Maps</a>`;
    },
    (err) => {
      output.innerHTML = "Error: " + err.message;
    },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  );
}
</script>
"""

st.components.v1.html(html_code, height=300)
st.caption("💡 Tip: On iPhone, tap 'Share → Add to Home Screen' for full GPS access.")
