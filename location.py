import streamlit as st
import json

st.set_page_config(page_title="📍 GPS Locator", page_icon="🌍")

st.title("📍 My GPS Location Tracker")
st.write("Press the button below to get your current location (latitude & longitude).")

# HTML + JS bridge to get location and post to Streamlit
gps_code = """
<script>
function sendLocationToStreamlit(latitude, longitude, accuracy) {
    const data = {lat: latitude, lon: longitude, acc: accuracy};
    const json = JSON.stringify(data);
    const streamlitEvent = new CustomEvent("streamlit:location", {detail: json});
    window.parent.document.dispatchEvent(streamlitEvent);
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const accuracy = position.coords.accuracy;
                sendLocationToStreamlit(latitude, longitude, accuracy);
            },
            function(error) {
                alert("Error getting location: " + error.message);
            },
            {
                enableHighAccuracy: true,
                timeout: 10000,
                maximumAge: 0
            }
        );
    } else {
        alert("Geolocation is not supported by this browser.");
    }
}
</script>
<button onclick="getLocation()">📍 Get My Location</button>
"""

# Inject HTML into Streamlit
st.components.v1.html(gps_code, height=100)

# Streamlit listener
st.markdown("### Output:")
location_data = st.session_state.get("location_data", None)

# JavaScript → Streamlit bridge using `st.experimental_data_editor` trick
loc_input = st.text_area("Hidden Data Exchange Box", key="hidden_box", label_visibility="collapsed")

if loc_input:
    try:
        data = json.loads(loc_input)
        lat, lon, acc = data["lat"], data["lon"], data["acc"]
        st.success(f"✅ Location Found!\n\n**Latitude:** {lat}\n**Longitude:** {lon}\n**Accuracy:** ±{acc:.1f} m")
        st.map({"lat": [lat], "lon": [lon]})
        st.markdown(f"[🌍 Open in Google Maps](https://www.google.com/maps?q={lat},{lon})")
    except Exception as e:
        st.warning("⚠️ Location data not received properly. Try again.")

st.caption("Note: Safari on iPhone may restrict GPS access. Works best on Chrome or Edge.")
