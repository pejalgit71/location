import streamlit as st
from streamlit_javascript import st_javascript

st.set_page_config(page_title="📍 My GPS Location", page_icon="🌍")

st.title("📍 My Current GPS Location")
st.write("Tap the button below to allow location access.")

# Ask browser for GPS
location = st_javascript(
    """
    async () => {
        if (!navigator.geolocation) {
            alert("Geolocation is not supported by your browser.");
            return null;
        }

        return new Promise((resolve, reject) => {
            navigator.geolocation.getCurrentPosition(
                (pos) => {
                    resolve({
                        latitude: pos.coords.latitude,
                        longitude: pos.coords.longitude,
                        accuracy: pos.coords.accuracy
                    });
                },
                (err) => {
                    alert("Error: " + err.message);
                    resolve(null);
                }
            );
        });
    }
    """
)

if location:
    lat = location.get("latitude")
    lon = location.get("longitude")
    acc = location.get("accuracy")
    st.success(f"✅ Location found!\n\n**Latitude:** {lat}\n**Longitude:** {lon}\n**Accuracy:** ±{acc:.1f} m")
    st.map({"lat": [lat], "lon": [lon]})
    st.markdown(f"[🌍 Open in Google Maps](https://www.google.com/maps?q={lat},{lon})")
else:
    st.info("Click the button and allow GPS permission.")
