import geopandas as gpd
import pandas as pd
from shapely.geometry import Point

# Cargar el GeoJSON original
gdf = gpd.read_file("SWF_2024_countries.geojson")

# Asegurarse de que el AUM es numérico
gdf["aum"] = pd.to_numeric(gdf["aum"], errors="coerce")

# Agrupar por país
agrupados = []
for country, grupo in gdf.groupby("country"):
    grupo = grupo.sort_values("aum", ascending=False)
    
    props = {
        "country": country,
        "aum_total": round(grupo["aum"].sum(), 2),
        "aum_total_formated": f"${grupo['aum'].sum():,.2f} billions"
    }

    for i, row in enumerate(grupo.itertuples(), 1):
        nombre = row.name
        aum = row.aum
        if pd.notna(aum):
            props[f"funds_{i}"] = f"{nombre} (${aum} bn)"
        else:
            props[f"funds_{i}"] = nombre
    
    geom = grupo.geometry.iloc[0]
    agrupados.append((props, geom))

# Crear nuevo GeoDataFrame
df_out = gpd.GeoDataFrame(
    [x[0] for x in agrupados], geometry=[x[1] for x in agrupados], crs="EPSG:4326"
)

# Guardar como GeoJSON
df_out.to_file("fondos_por_pais.geojson", driver="GeoJSON")

print("✅ Archivo 'fondos_por_pais.geojson' generado con éxito.")