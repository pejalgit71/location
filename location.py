import streamlit as st
from streamlit_js_eval import streamlit_js_eval

st.title("📍 GPS Tracker – Working on Mobile")

# Run JS to get GPS
location = streamlit_js_eval(
    js_expressions="""
        new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                pos => resolve({
                    lat: pos.coords.latitude,
                    lon: pos.coords.longitude,
                    acc: pos.coords.accuracy
                }),
                err => resolve(null),
                { enableHighAccuracy: true }
            );
        });
    """,
    key="get_gps",
)

if location:
    st.success("GPS Received!")
    lat = location["lat"]
    lon = location["lon"]
    acc = location["acc"]
    
    st.write("Latitude:", lat)
    st.write("Longitude:", lon)
    st.write("Accuracy:", acc, "m")

    st.map({"lat": [lat], "lon": [lon]})
else:
    st.info("Click 'Allow' when your browser asks for location.")
