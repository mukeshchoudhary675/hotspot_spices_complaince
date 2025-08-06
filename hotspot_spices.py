import streamlit as st
import pandas as pd
import folium
from streamlit_folium import st_folium
import json

# Title
st.title("🗺️ District Compliance Hotspot Map (India)")

# Upload Excel file
uploaded_file = st.file_uploader("Upload Excel File", type=["xlsx"])

# Upload GeoJSON file
geojson_file = st.file_uploader("Upload India District GeoJSON", type=["geojson", "json"])

if uploaded_file and geojson_file:
    df = pd.read_excel(uploaded_file)

    # Ensure column names
    required_columns = ['State', 'District', 'Compliance %']
    if not all(col in df.columns for col in required_columns):
        st.error(f"Excel must contain these columns: {', '.join(required_columns)}")
        st.stop()

    # Load GeoJSON
    geojson_data = json.load(geojson_file)

    # Normalize district names for merge (you can add more cleaning if needed)
    df['District'] = df['District'].str.strip().str.lower()
    df['Compliance %'] = df['Compliance %'].astype(float)

    # Create map
    m = folium.Map(location=[23.5937, 80.9629], zoom_start=5)

    folium.Choropleth(
        geo_data=geojson_data,
        data=df,
        columns=["District", "Compliance %"],
        key_on="feature.properties.DISTRICT",  # Adjust key if needed
        fill_color='YlGn',
        fill_opacity=0.7,
        line_opacity=0.2,
        legend_name='Compliance %',
        nan_fill_color='gray',
        highlight=True,
    ).add_to(m)

    # Show map
    st_folium(m, width=800, height=600)

    # Download button
    map_html = m._repr_html_()
    st.download_button(
        label="Download Map as HTML",
        data=map_html,
        file_name="district_compliance_map.html",
        mime="text/html"
    )
else:
    st.info("Upload both Excel and GeoJSON files to get started.")
