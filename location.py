import streamlit as st

st.set_page_config(page_title="📍 My GPS Location", page_icon="🌍")

st.title("📍 My Current GPS Location -faizal")
st.write("Tap the button below to share your live location.")

# Create a placeholder for coordinates
placeholder = st.empty()

# HTML + JS block to get location and send to Streamlit
location_html = """
<script>
function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(
            function(position) {
                const latitude = position.coords.latitude;
                const longitude = position.coords.longitude;
                const streamlitInput = window.parent.document.querySelector('input[data-testid="stTextInput-input"]');
                const hiddenLatLon = latitude + "," + longitude;
                const inputEvent = new Event("input", { bubbles: true });
                streamlitInput.value = hiddenLatLon;
                streamlitInput.dispatchEvent(inputEvent);
            },
            function(error) {
                alert("Error getting location: " + error.message);
            }
        );
    } else {
        alert("Geolocation not supported by this browser.");
    }
}
</script>

<button onclick="getLocation()">📍 Get My Location</button>
"""

st.components.v1.html(location_html, height=100)

# Hidden text input to receive data from JS
coords = st.text_input("Coordinates (auto-filled)", value="", label_visibility="collapsed")

if coords:
    try:
        lat, lon = map(float, coords.split(","))
        st.success(f"✅ Location found!\n\n**Latitude:** {lat}\n**Longitude:** {lon}")
        st.map({"lat": [lat], "lon": [lon]})
        st.markdown(f"[Open in Google Maps](https://www.google.com/maps?q={lat},{lon})")
    except:
        st.error("Could not parse GPS data. Try again.")
else:
    st.info("Click the button and allow location permission.")
