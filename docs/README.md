# Browntail Technical Documentation
### Carrie Nguyen

# Create Virtual Environment
This project code was generated using `Python 3.9.13`. Several dependencies are needed to plot the data using Geopandas. It is therefore easiest to generate a virtual environment to run the code.

1. In the terminal make a virtual environment by running:
	```
	python -m venv browntail
	```
2. Start the virtual environment by running:
	```
	source browntail/bin/activate
	```
3. Install the project dependencies located in the `requirements.txt` file using:
	```
	pip install -r requirements.txt
	```
The required dependencies should now be installed into the environment and should be ready to run the rest of the source code!

# Get Data
Get the required data files using 
```
make data
```
This should generate the following datasets that we are going to use:
- Bartlett dataset - public survey dataset with 602 entries
- MSFS dataset - subset of MSFS browntail dataset with 35 entries 
- Citizen dataset - private survey dataset with 476 entries
- Maine_Town_and_Townships_Boundary_Polygons_Feature - base map information from the [Maine.gov GeoLibrary](https://www.maine.gov/geolib/catalog.html#boundaries)

**Because of the residential address information in the Citizen survey, the raw (uncleaned) data files for the Citizen dataset are available on this public repository). The Makefile should be updated with the latest tokens for downloading the data, but new ones may be have to be generated**

# Data Cleaning
Clean the three datasets and create one large combined dataset by running 
```
make clean_data
```
Each dataset has to be cleaned slightly differently and the code addresses each datasets needs separately. The bulk of this project was devoted to resolving inconsistencies between the datasets.

## Bartlett Data

We first subet the columns of data that we want and rename them to clean them up. The following columns are kept in the Bartlett data:
- Longitude - longitude of tree sampled
- Latitude - latitude of tree sampled
- Common Name - common species name of tree sampled
- Condition Class - condition of tree sampled
- Observed BTM nests - number of nests observed in tree sampled
- Tree type - type of tree sampled 
- Entry source - Bartlett

We then clean up the Entry Source column by shortening the names to just Bartlett (we don't need the extra info).

The only other thing that we need to do is clean up the Common Name column by renaming the trees to their more general species. This will allow us to combine the Bartlett data with the other datasets for which we don't have such specific tree species information. 

After these processes, the Bartlett dataset is now cleaned and exported to a CSV file.

## MSFS Data

In the MSFS datset, we also subset the columns of interest and rename them. The following columns were selected from the MSFS data:
- Longitude - longitude of tree sampled
- Latitude - latitude of tree sampled
- Common Name - common species name of tree sampled
- Condition Class - condition of tree sampled
- Observed BTM nests - number of nests observed in tree sampled

We then impute the Tree type information from the Common name column and add it as a new column to the dataset.

The only other thing we need to do is add another column to the dataset, indicating the Entry source, which is MSFS.

The MSFS dataset is now cleaned and is exported to a CSV file.

## Citizen Data

The Citizen dataset is the most complicated to clean because it contains many inconsistencies and missing values. This is the reality of real datasets, especially those not sampled by professional sources (like Bartlett and MSFS). 

We start out by dropping completely empty rows in the data.

A lot of our samples are missing latitude and longitude data - but we can impute these values using info from the Address column if we have it for the sample. We first start out by identifying which samples have a lack of longitude or latitude data and save their indexes in a list.

Next, we use `geopy`'s ' `Nomatim()` function to impute the lat/lon data from each address associated with each index we identified above. We make sure to add `Waterville` to the address string so that the correct location coordinates are returned. All lat/lon info is then assigned back to the sample's Latitude and Longitude columns.

The following columns are selected and renamed:
- Longitude - longitude of tree sampled
- Latitude - latitude of tree sampled
- Common Name- tree species infected with BTMs on the property
- Obs_btm_trees - number of tree species infected with BTMs on the property
- Tree type - type of tree sampled

We add a Entry source column indicating each sample came from the `Citizen` survey. We also rename the values in the `tree_type` column to reflect the same naming system in the other datasets.

We then clean up any residual weird values and get rid of any samples in the dataset that we were not able to generate any location data.

This is a good checkpoint to take a look at our data before moving onward and it also fixes a weird indexing issue I kept running into as the result of dropped rows.

The `common_name` column contains a list of all the BTM infested tree speciess found on the resident's property. We want to plot each individual tree so we need to split the string of species and create new entries for each unique tree. After some string manipulation, we create separate entries using `pd.explode()`, which creates a new entry for each unique species but copies over all the shared data. To avoid indexing issues, we also reset the index of the dataframe using `.reset_index()`.

`pd.explode()` worked great, but it also copied over `tree_type` data, which is not necessarily shared across all of the trees at one residential property. This means that we have to impute the tree types, based on the common species name of the tree. 

We're almost done! We just remove any extra indexing columns created along the way and then export our cleaned dataset. 

# Combined BTM Data
The whole point of cleaning all of our datasets in a specific manner was to get them into a format where they could all be combined into one dataset. We can then use this dataset for plotting and other calculations in the future. 

We concatenate all of our cleaned datasets and select the columns of interest we will use in plotting our maps. The resulting dataframe is then exported as a CSV. 

# Mapping
Now that we have the data cleaned up, we can plot it using Geopandas.

## Surveyor Plot
Let's plot each of the BTM infected trees by their entry source:

```
make surveyor_plot
```

<img src="/figs/surveyor_plot.png">

We start out be reading in the data that we are working with here: 
- `btm_combined_df` - the cleaned and combined BTM data; this are the points we are plotting
- `df` - shapefile data from [Maine.gov GeoLibrary](https://www.maine.gov/geolib/catalog.html#boundaries); this contains the map plot information for Watervile

_Note: The shapefile data requires that 3 separate file structure (`_.shp`,` _.shx`, `_.dbf`) are all saved in the same directory in order for it to be plotted in Geopandas. Everything is saved in the `.zip` file, so it should be ok here._

The shapefile dataset includes plottable polygons for each town in Maine. We subset the dataset, to grab only the polygon associated with Waterville. 

Next, we convert `btm_combined_df` into a form that is plottable in Geopandas. To do this, we have to convert it into a GeoDataFrame. We specify our standard coordinate system using `crs`. `GeoDataFrame` creates an extra column containing plottable point data based on the Latitude and Longitude data from the original dataframe. 

Finally, we can plot our surveyor map. We first plot the Waterville polygon in light gray. We then overlay a basemap of Waterville using `contextily`. Finally, we plot our datapoints from our new GeoDataFrame object, colored by Entry source.

The map is then saved into the `figs` directory. 

## Species Plot
Let's plot the BTM infected trees by their common species name:

```
make species_plot
```

<img src="/figs/species_plot.png">

The species plot is generated in the same way as the surveyor plot above. The only difference is that we plot our datapoints from the GeoDataFrame object, colored by Commmon name.

The map is then saved into the `figs` directory. 

## Tree Type Plot
Let's plot each of BTM infected trees by their tree type:

```
make tree_type_plot
```

<img src="/figs/tree_type_plot.png">


The tree type plot is generated in the same way as the surveyor plot above. The only difference is that we plot our datapoints from the GeoDataFrame object, colored by Tree type.

The map is then saved into the `figs` directory. 

## Light Pollution Plot

As of yet, I have not been able to locate a light pollution map of Waterville with high enough resolution for satisfactory analysis.

<img src="/figs/bad_light_pollution_plot.png" width = 400x>

Here is a plot generated using ViirsEarthAtNight2012 data in `contextily`

`cx.add_basemap(ax, source=cx.providers.NASAGIBS.ViirsEarthAtNight2012, crs = waterville.crs)`

Updated versions of VIIRS exist with higher resolution, but exist only in GIS format. In the future, I am planning to learn more GIS to be able to obtain a higher quality map that I can import into Geopandas.  

# Remove data
Clean out all the datasets used using:
```
make clean
```

# Acknowledgements

- Thanks to Thom Klepach for allowing me to use and explore this dataset. 
- Thanks to Amanda Stent and Stephanie Taylor for their guidance and support throughout this project. 
- Thanks to Tahiya Chowdhury in assisting me with Geopandas troubleshooting. 
- Thanks to Philip Bogden for teaching me the tools to build this project and grow in my data science journey.
