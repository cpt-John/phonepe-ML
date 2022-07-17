import folium
import pandas as pd
import streamlit as st
from streamlit_folium import folium_static
from model import predict
from datetime import date, datetime


st.set_page_config(layout="wide")
json1 = f"states_india.geojson"

m = folium.Map(location=[23.47, 77.94], tiles='CartoDB positron', name="Light Map",
               zoom_start=5,
               attr='My Data Attribution')

option_map = {"count": 1,
              "amount": 2,
              "registration": 3}
st.markdown(
    '<style>.block-container{padding-top: 1.3em;padding-bottom: 2em;}</style>', unsafe_allow_html=True)
st.markdown("<h1 style='text-align: center; margin-top:0; padding:0'>PhonePe Prediction</h1>",
            unsafe_allow_html=True)

r1c1, r1c2, r1c3 = st.columns((1, 1, 4))
with r1c1:
    predict_date = st.date_input(
        "Prediction date",
        datetime.now(),
        max_value=datetime.strptime("2025-01-01", "%Y-%m-%d"),
        min_value=datetime.now(),
    )
with r1c2:
    selected_item = st.selectbox(
        "Select Transaction parameter",
        ["count",
         "amount",
         "registration", ],
        index=0,)
states_data = predict(option_map[selected_item], predict_date)

folium.Choropleth(
    geo_data=json1,
    name="choropleth",
    data=states_data,
    columns=["state_code", "value"],
    key_on="feature.properties.state_code",
    fill_color="Blues",
    fill_opacity=0.7,
    line_opacity=.1,
).add_to(m)
geo_json = folium.features.GeoJson('states_india.geojson', name="LSOA Code",
                                   popup=folium.features.GeoJsonPopup(fields=['st_nm']))
geo_json.add_to(m)
r2c1, r2c2, = st.columns((1, 3))

map_vals = \
    {0: 'Andaman and Nicobar',
     1: 'Andhra Pradesh',
     2: 'Arunachal Pradesh',
     3: 'Assam',
     4: 'Bihar',
     5: 'Chandigarh',
     6: 'Chhattisgarh',
     7: 'Daman and Diu',
     8: 'Delhi',
     9: 'Goa',
     10: 'Gujarat',
     11: 'Haryana',
     12: 'Himachal Pradesh',
     13: 'Jammu and Kashmir',
     14: 'Jharkhand',
     15: 'Karnataka',
     16: 'Kerala',
     17: 'Ladakh',
     18: 'Lakshadweep',
     19: 'Madhya Pradesh',
     20: 'Maharashtra',
     21: 'Manipur',
     22: 'Meghalaya',
     23: 'Mizoram',
     24: 'Nagaland',
     25: 'Odisha',
     26: 'Puducherry',
     27: 'Punjab',
     28: 'Rajasthan',
     29: 'Sikkim',
     30: 'Tamil Nadu',
     31: 'Telangana',
     32: 'Tripura',
     33: 'Uttar Pradesh',
     34: 'Uttarakhand',
     35: 'West Bengal'}

with r2c1:
    states_data['state'] = states_data.replace(
        {'state_code': map_vals})['state_code']
    states_data.drop("state_code", axis=1, inplace=True)
    st.table(states_data)
with r2c2:
    folium_static(m, width=1600, height=950)
