import streamlit as st

st.set_page_config(page_title="📍 GPS Map Tracker", page_icon="🗺️")
st.title("📍 My GPS Location Tracker")
st.write("Tap the button to get your GPS location and see it on the map.")

# HTML + JS block with Leaflet map
html_code = """
<div id="map" style="height: 500px;"></div>
<button onclick="getLocation()">📍 Get My Location</button>
<p id="coords">Waiting for location...</p>

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
  if (!navigator.geolocation) {
    alert("Geolocation not supported.");
    return;
  }
  navigator.geolocation.getCurrentPosition(
    (pos) => {
      const lat = pos.coords.latitude;
      const lon = pos.coords.longitude;
      const acc = pos.coords.accuracy;
      document.getElementById('coords').innerHTML =
        `Latitude: ${lat.toFixed(6)}<br>Longitude: ${lon.toFixed(6)}<br>Accuracy: ±${acc.toFixed(1)} m`;
      
      map.setView([lat, lon], 16);
      if (marker) { map.removeLayer(marker); }
      marker = L.marker([lat, lon]).addTo(map)
        .bindPopup(`📍 You are here<br>Accuracy ±${acc.toFixed(1)} m`)
        .openPopup();
    },
    (err) => { alert("Error: " + err.message); },
    { enableHighAccuracy: true, timeout: 10000, maximumAge: 0 }
  );
}
</script>
"""

st.components.v1.html(html_code, height=600)
st.caption("Works on iPhone Safari, Android Chrome, Desktop. Fully interactive map.")
