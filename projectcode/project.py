#to be coded
#..
import geopandas
import os
# Check available maps

import pandas as pd
import geopandas as gpd
import matplotlib.pyplot as plt


geopandas.datasets.available
data = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/mergedata.csv")


# Selecting a particular map
maryland_map = gpd.read_file("/Users/karlyjae/Documents/25-spring-kiriarte/MDshape/Maryland_Physical_Boundaries_-_County_Boundaries_(Detailed).shp")

# Display basic map
maryland_map.plot()
plt.show()

print(maryland_map.columns)
print(maryland_map["COUNTY"].unique())
# Plot the subset
#usa.plot();
#print(d