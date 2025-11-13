import streamlit as st

# Page setup
st.set_page_config(page_title="My GPS Location", page_icon="📍", layout="centered")

st.title("📍 My Current GPS Location")
st.write("Tap the button below to share your location.")

# Add a placeholder for displaying coordinates
latitude = st.empty()
longitude = st.empty()
map_placeholder = st.empty()

# JavaScript to get location from browser
get_location_js = """
<script>
var showLocation = function (position) {
    const latitude = position.coords.latitude;
    const longitude = position.coords.longitude;
    var coordinates = latitude + "," + longitude;
    window.parent.postMessage({latitude: latitude, longitude: longitude}, "*");
};

function errorHandler(err) {
    if(err.code == 1) {
        alert("Error: Access to location is denied!");
    } else if( err.code == 2) {
        alert("Error: Position unavailable!");
    }
}

function getLocation() {
    if (navigator.geolocation) {
        navigator.geolocation.getCurrentPosition(showLocation, errorHandler);
    } else {
        alert("Sorry, your browser does not support geolocation!");
    }
}
</script>
<button onclick="getLocation()">Get My Location</button>
"""

# Inject the JS
st.components.v1.html(get_location_js, height=100)

# Receive coordinates from JS
location_data = st.experimental_get_query_params()
if 'latitude' in location_data and 'longitude' in location_data:
    lat = float(location_data['latitude'][0])
    lon = float(location_data['longitude'][0])
    latitude.write(f"**Latitude:** {lat}")
    longitude.write(f"**Longitude:** {lon}")
    map_placeholder.map({"lat": [lat], "lon": [lon]})
else:
    st.info("Click the button to allow location access.")
