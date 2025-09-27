import pandas as pd
import geopandas as gpd
from shapely.geometry import Point

# esto carga el Excel
df = pd.read_excel("SWF_2024_data.xlsx", sheet_name="B")

# esto crea los puntos a partir de la longtud y la latitud
geometry = [Point(xy) for xy in zip(df["longitude"], df["latitude"])]

# esto crea GeoDataFrame
gdf = gpd.GeoDataFrame(df, geometry=geometry, crs="EPSG:4326")

# esto exporta a Geojson
gdf.to_file("SWF_2024_countries.geojson", driver="GeoJSON")

# esto es un mensaje de éxito, si es que todo ha salido bien
print("Lo hemos conseguido, tienes tu archivo en geojson!")