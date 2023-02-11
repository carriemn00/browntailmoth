# load libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci
import contextily as cx
import geopandas as gpd
from shapely.geometry import Point, Polygon
plt.ioff()

# import datasets
btm_combined = pd.read_csv('data/btm_combined.csv')

# obtain base shape map for city of Waterville
# Note: the following must all be saved in the same directory
# _.shp
# _.shx
# _.dbf
df = gpd.read_file('data/Maine_Town_and_Townships_Boundary_Polygons_Feature.zip')

# subset to grab Waterville poly
waterville = df[df['TOWN'] == 'Waterville']

# use Shapely to transform lat and lon data into geometric points for each datset
crs = {'init':'EPSG:4326'}
btm_combined_df = gpd.GeoDataFrame(btm_combined, crs = crs,geometry = [Point(xy) for xy in zip(btm_combined['lon'], btm_combined['lat'])])

ax = waterville.plot(figsize = (10,10), cmap = 'gray', alpha = 0.25, edgecolor = 'k')
cx.add_basemap(ax, source=cx.providers.Stamen.Terrain, crs = waterville.crs)
btm_combined_df.plot('tree_type', cmap = 'Spectral',ax = ax, alpha = 1, legend = True)
ax.set_title('Tree Type')

plt.savefig('figs/tree_type_plot.jpg')
plt.show();
