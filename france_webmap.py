import streamlit as st
import folium
import requests
from folium.plugins import MarkerCluster
import pandas as pd
import geopandas as gpd 
from shapely.geometry import Point, LineString
import json 
import matplotlib.pyplot as plt
import ipywidgets
from IPython.display import HTML, display

m = folium.Map(location=[46.2276, 2.2137], tiles="OpenStreetMap", zoom_start=5.5)
shp_map1 = gpd.read_file("C:/Users/DELL/OneDrive - WASCAL/Cours Paris Saclay/Dossier de stage BETA/15_30_km_csv/compiegne_30km.shp")
shp_map2 = gpd.read_file("C:/Users/DELL/OneDrive - WASCAL/Cours Paris Saclay/Dossier de stage BETA/15_30_km_csv/compiegne_15km.shp")

data_30km = pd.read_csv("C:/Users/DELL/OneDrive - WASCAL/Cours Paris Saclay/Dossier de stage BETA/15_30_km_csv/30km_all_failed.csv")
data_15km = pd.read_csv("C:/Users/DELL/OneDrive - WASCAL/Cours Paris Saclay/Dossier de stage BETA/15_30_km_csv/15km_all_failed.csv")

folium.GeoJson(data=shp_map1).add_to(m)


folium.Choropleth(shp_map1,
                 data = data_30km,
                 key_on="feature.properties.code",
                 columns = ["code","Population"],
                 fill_color='RdPu',
                 line_weight=0.1,
                 line_opacity=0.5,
                 legend_name='Population 1',
                 name = "Population dans un rayon de 30 km autour de la Forêt de Compiègne").add_to(m)


r = folium.Choropleth(shp_map2,
                 data = data_15km,
                 key_on="feature.properties.code",
                 columns = ["code","Population municipale 2021"],
                 fill_color='RdPu',
                 line_weight=0.1,
                 line_opacity=0.5,         
                 name = "Population dans un rayon de 15 km autour de la Forêt de Compiègne").add_to(m)

for key in r._children:
    if key.startswith('color_map'):
        del(r._children[key])
        
        
# add the markers to the map 

# location1 = df_counters[['latitude', 'longitude']]
# locationlist = locations.values.tolist()
# len(locationlist)

# Create an output widget
out = ipywidgets.Output(layout={'border': '1px solid black'})

# Create a dropdown widget with options as rows of the DataFrame
w = ipywidgets.Dropdown(
    options=data_30km.index.values.tolist(),  # Use index values instead of column names
    value=data_30km.index.values[0],  # Set default value to the first row index
    description='Les Communes:',
    disabled=False,
)

# Define a function to handle dropdown change
def on_dropdown_change(change):
    out.clear_output()
    with out:
        # Display the selected row using the row index
        display(data_30km.loc[w.value])  

# Observe the dropdown widget for changes
w.observe(on_dropdown_change, names='value')

# Display the dropdown widget
display(w)

# Display the output widget
display(out)

folium.LayerControl().add_to(m)

# save the map
#m.save("footprint.html")