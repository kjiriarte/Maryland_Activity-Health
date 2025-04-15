#to be coded
#..
import geopandas
import os
#import geodatasets
# Check available maps

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt
import seaborn as sns
import folium
from sklearn.linear_model import RidgeCV
from sklearn.preprocessing import StandardScaler
from sklearn.metrics import r2_score


print(geopandas.datasets.available)
data = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mergedata.csv")
data.rename(columns={'Jurisdiction': 'County'}, inplace=True)
data2 = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mapdata.csv")
data2_subset = data2.drop("Jurisdiction", axis=1)
# Selecting a particular map


columns_to_keep = ['Jurisdiction', 'Number_of_Parks', 'Amount', 'Median Household Income ($)','Percent Families in Poverty', 'Total Population',
'White Alone', 'Black Alone','TOTAL Publicly Owned', 'All races/ ethnicities (aggregated)', 'Black or African American Non-Hispanic/Latino', 'White Non-Hispanic/Latino',
"Percent Walked", "Unemployment Rate",
 "Percent Civilian Population w/ Health Ins. Cov.", "Bachelor's degree"]

dataused = data2.filter(items=columns_to_keep)
datausedmatrix = dataused.drop(columns=['Jurisdiction'], errors = 'ignore')

datausedmatrix.rename(columns={'Number_of_Parks': '# of Parks', 'Percent Families in Poverty': 'Poverty %', 'TOTAL Publicly Owned': 'Public (Acres)',
}, inplace=True)


#print(data2.columns.tolist())

#print(datausedmatrix.columns.tolist())
#datausedmatrix = datausedmatrix.drop(columns=['[]'])
#print(datausedmatrix.columns.tolist())

dataused.to_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/dataused.csv", index = False)


#correlation matrix -- to be used for heatmap later
datausedmatrix = datausedmatrix.corr().round(2)

#matrix.style.background_gradient()

#heatmap - will narrow down variables

sns.heatmap(datausedmatrix, vmin=0, cmap='Greens')
#pd.plotting.scatter_matrix(datausedmatrix, figsize=(8,8))
plt.show()
#print(maryland_map.columns)
#print(maryland_map["COUNTY"].unique())
# Plot the subset
#usa.plot();
#print(d

#Making Maps 


data1 = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/maryland_trail_accessibility_by_county.csv")

data1.rename(columns={'name_right': 'Jurisdiction'}, inplace=True)

m = folium.Map(location=[39.0, -76.7], zoom_start=7, tiles="CartoDB positron")

merged_df = dataused.merge(data1, on='Jurisdiction', how='outer')
#dataused.to_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mergedf.csv", index = False)


#trail_lookup = dict(zip(data["name_right"], data["num_trails"]))

     
folium.Choropleth(
            geo_data="/Users/karlyjae/Documents/25-spring-kiriarte/MDshape/maryland-counties.geojson",
            name="choropleth",
            data=data1,
            columns=["Jurisdiction", "accessibility_score"],
            key_on="feature.properties.name",  
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Acessibility Score"
    ).add_to(m)

folium.GeoJson(
    "/Users/karlyjae/Documents/25-spring-kiriarte/MDshape/maryland-counties.geojson",
    name="Counties",
    style_function=lambda x: {
        "fillColor": "transparent",
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["name"],  
        aliases=["County:"],
        sticky=False,
        labels=True
    )
).add_to(m)

m.save("maryland_map.html")

datapark = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/dataused.csv")

m2 = folium.Map(location=[39.0, -76.7], zoom_start=7, tiles="CartoDB positron")

  
folium.Choropleth(
            geo_data="/Users/karlyjae/Documents/25-spring-kiriarte/MDshape/maryland-counties.geojson",
            name="choropleth",
            data=datapark,
            columns=["Jurisdiction", "All races/ ethnicities (aggregated)"],
            key_on="feature.properties.name",  # Or another property in your GeoJSON
            fill_color="YlGn",
            fill_opacity=0.7,
            line_opacity=0.2,
            legend_name="Your Data Legend"
    ).add_to(m2)

folium.GeoJson(
    "/Users/karlyjae/Documents/25-spring-kiriarte/MDshape/maryland-counties.geojson",
    name="Counties",
    style_function=lambda x: {
        "fillColor": "transparent",
        "color": "black",
        "weight": 0.5,
        "fillOpacity": 0
    },
    tooltip=folium.GeoJsonTooltip(
        fields=["name"], 
        aliases=["County:"],
        sticky=False,
        labels=True
    )
).add_to(m2)



m2.save("Parksmaryland_map.html")