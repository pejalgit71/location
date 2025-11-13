import streamlit as st
import folium

st.set_page_config(page_title="📍 GPS Map Tracker", page_icon="🗺️")

st.title("📍 My GPS Location Tracker")
st.write("Tap the button below to get your GPS coordinates and view your location on a live map.")

# HTML + JS block for location retrieval
gps_html = """
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

# Inject the HTML button
st.components.v1.html(gps_html, height=150)

# Hidden field to store coordinates
coords = st.text_area("Hidden GPS data", label_visibility="collapsed")

if coords:
    try:
        lat, lon, acc = map(float, coords.split(","))
        st.success(f"✅ Location Found! Accuracy ±{acc:.1f} m")
        st.write(f"**Latitude:** {lat}")
        st.write(f"**Longitude:** {lon}")

        # Create folium map manually
        map_center = [lat, lon]
        m = folium.Map(location=map_center, zoom_start=17, control_scale=True)
        folium.Marker(
            map_center,
            popup=f"📍 You are here<br>Lat: {lat}<br>Lon: {lon}<br>Accuracy: ±{acc:.1f} m",
            icon=folium.Icon(color="red", icon="info-sign")
        ).add_to(m)

        # Convert to HTML string and display
        map_html = m._repr_html_()
        st.components.v1.html(map_html, height=500)

        # Add a link to Google Maps
        st.markdown(f"[🌍 Open in Google Maps](https://www.google.com/maps?q={lat},{lon})")

    except Exception as e:
        st.warning("⚠️ Could not render the map properly. Try again.")
else:
    st.info("Click the button to allow GPS access.")
