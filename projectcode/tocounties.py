import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# Step 1: Load your trail data (make sure this file has lat/lng columns)
df_trails = pd.read_csv("/Users/karlyjae/Documents/25-spring-kiriarte/datasets/Maryland.csv")  # e.g. "Maryland.csv"

# If your file uses different column names, adjust accordingly:
lat_col = "_geoloc/lat"
lng_col = "_geoloc/lng"

# Step 2: Convert trail DataFrame to GeoDataFrame using coordinates
geometry = [Point(xy) for xy in zip(df_trails[lng_col], df_trails[lat_col])]
gdf_trails = gpd.GeoDataFrame(df_trails, geometry=geometry, crs="EPSG:4326")  # WGS84

# Step 3: Load public Maryland county GeoJSON
# GitHub raw file (use raw link to download directly)
geojson_url = "https://raw.githubusercontent.com/frankrowe/maryland-geojson/master/maryland-counties.geojson"
gdf_counties = gpd.read_file(geojson_url)

# Step 4: Spatial join - assign each trail to a county
gdf_joined = gpd.sjoin(gdf_trails, gdf_counties, how="left", predicate="within")


# Step 5: Aggregate trail data by county
df_county_trails = gdf_joined.groupby("name_right").agg(
    num_trails=("trail_id", "count"),
    total_length=("length", "sum"),
    avg_difficulty=("difficulty_rating", "mean"),
    avg_rating=("avg_rating", "mean"),
    total_popularity=("popularity", "sum")
).reset_index()

# Step 6: Create accessibility score (custom logic – modify as needed)
df_county_trails["accessibility_score"] = (
    df_county_trails["total_length"] * df_county_trails["avg_rating"]
) / df_county_trails["avg_difficulty"]

# Preview result
print(df_county_trails.head())

# Optional: Save to CSV for use in modeling
df_county_trails.to_csv("maryland_trail_accessibility_by_county.csv", index=False)