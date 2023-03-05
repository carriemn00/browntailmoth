#### Citizen Survey 2021 Data Cleaning
#### Carrie Nguyen
#### 2022-2023

# load libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci
plt.ioff()

citizen_2021 = pd.read_csv('https://raw.githubusercontent.com/carriemn00/browntailmoth/main/data/citizen_clean.csv')
print(citizen_2021.shape)

# drop completely empty rows: 333 and onward
citizen_2021 = citizen_2021.dropna(how='all')

# identify which samples have lack of lon/lat data
missing_latlon = np.where(np.isnan(citizen_2021['Latitude']) | np.isnan(citizen_2021['Longitude']))[0]
print(missing_latlon)

# impute missing lat/lon values
from geopy.geocoders import Nominatim
geolocator = Nominatim(user_agent = 'latlon')
print('samples missing latlon: ', len(missing_latlon))

for i in range(len(missing_latlon)):
  print(i)
  print('index into: ', missing_latlon[i])
  location = geolocator.geocode(citizen_2021.iloc[missing_latlon[i],1] + ', Waterville')
  print(location)
  if location is None:
    # create dummy variables 
    citizen_2021.iloc[missing_latlon[i],2] = np.nan
    citizen_2021.iloc[missing_latlon[i],3] = np.nan
    # save idx
    remove_idx = missing_latlon[i]
    continue
  
  citizen_2021.iloc[missing_latlon[i],2] = location.longitude
  citizen_2021.iloc[missing_latlon[i],3] = location.latitude

  # subset the columns that we want
citizen_2021 = citizen_2021[['Longitude', 'Latitude', 'BTM positive trees',
                             'Tree Category (1: Ornamental/ LargeTree 2: Flowering/ Fruiting      3: Bush         4: Mixed']]

# clean up col names
citizen_2021 = citizen_2021.rename(columns = {'Longitude': 'lon', 'Latitude': 'lat', 'BTM positive trees': 'common_name',  
                                    'Tree Category (1: Ornamental/ LargeTree 2: Flowering/ Fruiting      3: Bush         4: Mixed': 'tree_type'})

# insert col for entry source
citizen_2021.insert(4, 'entry_source', np.full((citizen_2021.shape[0], 1), 'Citizen Survey 2021'))

# fix wonky entry
citizen_2021.iloc[287,4] = np.NaN

# remove nans in data
# drop rows that has NaN values on lon or lat
citizen_2021=citizen_2021.dropna(subset=['lon','lat'])

# reset indices
citizen_2021.to_csv('temp_citizen_2021.csv')
citizen_2021 = pd.read_csv('*/temp_citizen_2021.csv')

print('before:', citizen_2021.shape)
# create separate entries for each tree: split common_name on comma
for i in range(len(citizen_2021)):
  print(i)
  # split on comma
  # print(i, ' common name is: ', citizen['common_name'][i])
  if (pd.isnull(citizen_2021['common_name'][i])):
    continue
  names = citizen_2021['common_name'][i].split(',')
  # remove spaces 
  names = [n.strip(' ') for n in names]
  names = names[:-1]
  print(names)
  # print('split: ', names)
  # citizen['common_name'][i] = names
  citizen_2021.at[i, 'common_name'] = names


# create separate entries
citizen_2021 = citizen_2021.explode('common_name')
print('after:', citizen_2021.shape)

citizen_2021 = citizen_2021.reset_index()

# rename tree types
citizen_2021['tree_type'] = citizen_2021['common_name'].map({'Crabapple': 'Fruiting / Flowering', 
                                  'Oak': 'Ornamental',
                                  'Maple': 'Ornamental',
                                  'Ash': 'Ornamental',
                                  'Birch': 'Ornamental',
                                  'Serviceberry': 'Ornamental',
                                  'Apple': 'Fruiting / Flowering',
                                  'Pear': 'Fruiting / Flowering',
                                  'Hawthorn': 'Fruiting / Flowering',
                                  'Cherry': 'Fruiting / Flowering',
                                  'Lilac': 'Fruiting / Flowering',
                                  'Linden': 'Fruiting / Flowering',
                                  'Elm': 'Ornamental',
                                  'Poplar': 'Ornamental',
                                  })

# subset cols again
citizen_2021  = citizen_2021[['lon', 'lat', 'common_name', 'tree_type', 'entry_source']]

# save csv
citizen_2021.to_csv('citizen_2021_clean.csv')