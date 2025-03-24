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


print(geopandas.datasets.available)
data = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mergedata.csv")
data.rename(columns={'Jurisdiction': 'County'}, inplace=True)
data2 = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mapdata.csv")
data2_subset = data2.drop("Jurisdiction", axis=1)
# Selecting a particular map
maryland_map = gpd.read_file("/Users/karlyjae/Documents/25-spring-kiriarte/MDshape/Maryland_Physical_Boundaries_-_County_Boundaries_(Detailed).shp")

maryland_map.plot()
# Display basic map
#maryland_map.plot(column='All races/ ethnicities (aggregated)')
#maryland_map.axis('off')
#fig = plt.figure(frameon=False)
#maryland_map = fig.add_axes([0, 0, 1, 1])
#maryland_map.axis('off')
plt.axis("off") 
#plt.show()
#print(data2_subset)

#correlation matrix -- to be used for heatmap later
matrix = data2_subset.corr().round(2)

matrix.style.background_gradient()

#heatmap - will narrow down variables
sns.heatmap(matrix)
#pd.plotting.scatter_matrix(matrix, figsize=(8,8))
#plt.show()
#print(maryland_map.columns)
#print(maryland_map["COUNTY"].unique())
# Plot the subset
#usa.plot();
#print(d