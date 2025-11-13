import streamlit as st
from streamlit_javascript import st_javascript

st.set_page_config(page_title="📍 My GPS Location", page_icon="🌍")

st.title("📍 My Current GPS Location")
st.write("Press the button to get your real-time GPS location.")

# Add a button
if st.button("📍 Get My Location"):
    st.write("Requesting location access... please wait and allow permission if asked.")

    # Run JavaScript safely after button click
    location = st_javascript("""
        async () => {
            return new Promise((resolve) => {
                if (!navigator.geolocation) {
                    alert("Geolocation not supported by your browser.");
                    resolve(null);
                } else {
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
                        },
                        {
                            enableHighAccuracy: true,
                            timeout: 10000,
                            maximumAge: 0
                        }
                    );
                }
            });
        }
    """)

    # Handle returned data
    if location:
        lat = location.get("latitude")
        lon = location.get("longitude")
        acc = location.get("accuracy")

        if lat and lon:
            st.success(f"✅ Location found!\n\n**Latitude:** {lat}\n**Longitude:** {lon}\n**Accuracy:** ±{acc:.1f} m")
            st.map({"lat": [lat], "lon": [lon]})
            st.markdown(f"[🌍 Open in Google Maps](https://www.google.com/maps?q={lat},{lon})")
        else:
            st.warning("⚠️ Location data was empty. Please refresh and try again.")
    else:
        st.error("❌ Could not get your location. Please ensure GPS permission is allowed in Safari settings.")
else:
    st.info("Click the button above to allow GPS access.")
