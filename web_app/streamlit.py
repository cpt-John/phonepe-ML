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
r2c1, r2c2, = st.columns((3, 1))

map_vals = \
    {0: 'Telangana',
     35: 'Andaman & Nicobar Island',
     28: 'Andhra Pradesh',
     12: 'Arunanchal Pradesh',
     18: 'Assam',
     10: 'Bihar',
     22: 'Chhattisgarh',
     25: 'Daman & Diu',
     30: 'Goa',
     24: 'Gujarat',
     6: 'Haryana',
     2: 'Himachal Pradesh',
     1: 'Jammu & Kashmir',
     20: 'Jharkhand',
     29: 'Karnataka',
     32: 'Kerala',
     31: 'Lakshadweep',
     23: 'Madhya Pradesh',
     27: 'Maharashtra',
     14: 'Manipur',
     4: 'Chandigarh',
     34: 'Puducherry',
     3: 'Punjab',
     8: 'Rajasthan',
     11: 'Sikkim',
     33: 'Tamil Nadu',
     16: 'Tripura',
     9: 'Uttar Pradesh',
     5: 'Uttarakhand',
     19: 'West Bengal',
     21: 'Odisha',
     26: 'Dadara & Nagar Havelli',
     17: 'Meghalaya',
     15: 'Mizoram',
     13: 'Nagaland',
     7: 'NCT of Delhi'}

with r2c2:
    states_data['state'] = states_data.replace(
        {'state_code': map_vals})['state_code']
    states_data.drop("state_code", axis=1, inplace=True)
    st.dataframe(states_data,)
with r2c1:
    folium_static(m, width=1200)
