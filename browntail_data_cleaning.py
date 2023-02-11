# load libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci
from geopy.geocoders import Nominatim
plt.ioff()

#### Bartlett Data ####
# private token is time-sensitive
bartlett = pd.read_csv('data/bartlett_raw.csv')
# print(bartlett.head)
# print(bartlett.shape)

# subset the columns that we want
bartlett = bartlett[['Longitude', 'Latitude', 'Common Name', 'Condition Class', 'ObservedBTMNests', 
    'Tree Type (Ornamental | Fruiting / Flowering | Bush)', 'Entry Source']]

# clean up col names
bartlett = bartlett.rename(columns = {'Longitude': 'lon', 'Latitude': 'lat', 'Common Name': 'common_name', 'Condition Class': 'condition_class', 
                           'ObservedBTMNests': 'obs_btm_nests', 'Tree Type (Ornamental | Fruiting / Flowering | Bush)': 'tree_type',
                           'Entry Source': 'entry_source'})
# rename entry source col
bartlett = bartlett.replace(regex = [r'^Bartlett.*$'], value = 'Bartlett')
bartlett

# rename common tree names
bartlett = bartlett.replace({'common_name': {'Crabapple ' : 'Crabapple', 'Elm-American ' : 'Elm',
                                           'Oak-Northern Red ' : 'Oak', 'Cherry-Black ' : 'Cherry',
                                           'Pear-Callery ' : 'Pear', 'Serviceberry ' : 'Serviceberry',
                                           'Birch-Paper ' : 'Birch', 'Oak-White ' : 'Oak',
                                           'Maple-Sugar ' : 'Maple', 'Poplar-Aspen ' : 'Poplar',
                                           'Elm-Chinese ' : 'Elm', 'Poplar-Bigtooth Aspen ' : 'Poplar',
                                           'Maple-Boxelder ' : 'Maple', "Maple-Freeman's " : 'Maple',
                                           'Maple-Norway ' : 'Maple', 'Maple-Red ' : 'Maple',
                                           'Ash-Green ' : 'Ash', 'Ash-White ' : 'Ash', 
                                           'Birch-River ' : 'Birch', 'Linden-Littleleaf ' : 'Linden', 
                                           'Ash-Black ' : 'Ash', 'Beech-American ' : 'Beech', 
                                           'Ginkgo ' : 'Ginkgo', 'Honeylocust-Thornless Common ' : 'Honeylocust',
                                           'Horsechestnut-Common ' : 'Horsechestnut', 'Lilac-Japanese Tree ' : 'Lilac',
                                           'Locust-Black ' : 'Locust', 'Maple-Silver ' : 'Maple',
                                           'Pine-Eastern White ' : 'Pine', 'Plum-Purple Leaf ' : 'Plum',
                                           'Spruce-Colorado Blue ' : 'Spruce', 'Willow ' : 'Willow'}})

# export cleaned data and move on to the next dataset
bartlett.to_csv('data/bartlett_clean.csv')

#### MSFS Data ####
# private token is time sensitive
msfs = pd.read_csv('data/msfs_raw.csv')
# print(msfs.head)
# print(msfs.shape)

# subset the columns that we want
msfs = msfs[['Longitude', 'Latitude', 'Host', 'Pattern', 'Count']]
# clean up col names
msfs = msfs.rename(columns = {'Longitude': 'lon', 'Latitude': 'lat', 'Host': 'common_name', 'Pattern': 'condition_class', 
                           'Count': 'obs_btm_nests'})

# Impute tree type info
tree_type = []
for i in range(len(msfs)):
  # print(msfs.iloc[i, 2])
  if msfs.iloc[i,2] == 'Oak':
    tree_type.append('Ornamental')
  if msfs.iloc[i,2] == 'Maple':
    tree_type.append('Fruiting / Flowering')
# print(tree_type)
msfs.insert(4, 'tree_type', tree_type)

# add entry source col
msfs.insert(6, 'entry_source', np.full((msfs.shape[0], 1), 'MSFS Winter Web Survey'))

# export cleaned data and move on to the next dataset
msfs.to_csv('data/msfs_clean.csv')

#### Citizen Data ####
# private token is time sensitive
citizen = pd.read_csv('data/citizen_raw.csv')
# print(citizen.head)
# print(citizen.shape)

# drop completely empty rows: 333 and onward
citizen = citizen.dropna(how='all')

# identify which samples have lack of lon/lat data
missing_latlon = np.where(np.isnan(citizen['Latitude']) | np.isnan(citizen['Longitude']))[0]
print('indexes of missing lat/lon: ', missing_latlon)

# impute missing lat/lon values
geolocator = Nominatim(user_agent = 'missing_latlon')
print('samples missing latlon: ', len(missing_latlon))

for i in range(len(missing_latlon)):
  print(i)
  print('index into: ', missing_latlon[i])
  location = geolocator.geocode(citizen.iloc[missing_latlon[i],1] + ', Waterville')
  print(location)
  if location is None:
    continue
  
  citizen.iloc[missing_latlon[i],2] = location.longitude
  citizen.iloc[missing_latlon[i],3] = location.latitude

# subset the columns that we want
citizen = citizen[['Longitude', 'Latitude', 'BTM positive trees', 'Number of BTM positive Tree Species', 
    'Tree Category (1: Ornamental/ LargeTree 2: Flowering/ Fruiting      3: Bush         4: Mixed']]

citizen 
# clean up col names
citizen = citizen.rename(columns = {'Longitude': 'lon', 'Latitude': 'lat', 'BTM positive trees': 'common_name',  
                           'Number of BTM positive Tree Species': 'obs_btm_trees', 'Tree Category (1: Ornamental/ LargeTree 2: Flowering/ Fruiting      3: Bush         4: Mixed': 'tree_type',
                           })

# add entry source
citizen.insert(5, 'entry_source', np.full((citizen.shape[0], 1), 'Citizen Survey'))

# rename tree types 
# 1: Ornamental/ LargeTree 2: Flowering/ Fruiting      3: Bush         4: Mixed
citizen = citizen.replace({'tree_type': {'1' : 'Ornamental', 
                               '2' : 'Fruiting / Flowering',
                               '3' : 'Bush',
                               '4' : 'Mixed'}})

# weird string in this cell; fix manually
citizen.iloc[287,4] = np.NaN

# remove nans in data
# drop rows that has NaN values on lon or lat
citizen=citizen.dropna(subset=['lon','lat'])

# this is a good checkpoint; also fixes indexing of dropped locations
citizen.to_csv('data/temp_citizen.csv')
citizen = pd.read_csv('data/temp_citizen.csv')

print('before:', citizen.shape)
# create separate entries for each tree: split common_name on comma
for i in range(len(citizen)):
  # split on comma
  # print(i, ' common name is: ', citizen['common_name'][i])
  if (pd.isnull(citizen['common_name'][i])):
    continue
  names = citizen['common_name'][i].split(',')
  # remove spaces 
  names = [n.strip(' ') for n in names]
  names = names[:-1]
  # print('split: ', names)
  # citizen['common_name'][i] = names
  citizen.at[i, 'common_name'] = names

# create separate entries
citizen = citizen.explode('common_name')
print('after:', citizen.shape)

# reset indices
citizen = citizen.reset_index()

# rename tree_types
# create separate entries for each tree: split common_name on comma
for i in range(len(citizen)):
  # print(i, ' ', citizen.iloc[i, 4])

  if (pd.isnull(citizen.iloc[i, 4])):
    citizen.at[i, 'tree_type'] = np.nan
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Crabapple'):
    citizen.at[i, 'tree_type'] = 'Fruiting / Flowering'
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Oak'):
    citizen.at[i, 'tree_type'] = 'Ornamental'
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Maple'):
    citizen.at[i, 'tree_type'] = 'Ornamental'
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Ash'):
    citizen.at[i, 'tree_type'] = 'Ornamental'
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Birch'):
    citizen.at[i, 'tree_type'] = 'Ornamental' 
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Serviceberry'):
    citizen.at[i, 'tree_type'] = 'Ornamental' 
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Apple'):
    citizen.at[i, 'tree_type'] = 'Fruiting / Flowering'
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Pear'):
    citizen.at[i, 'tree_type'] = 'Fruiting / Flowering'
    # print('replaced with: ', citizen.iloc[i,4])  
    continue
  if (citizen.iloc[i, 4] == 'Hawthorn'):
    citizen.at[i, 'tree_type'] = 'Fruiting / Flowering'
    # print('replaced with: ', citizen.iloc[i,4])
    continue
  if (citizen.iloc[i, 4] == 'Cherry'):
    citizen.at[i, 'tree_type'] = 'Fruiting / Flowering'
    # print('replaced with: ', citizen.iloc[i,4])
    continue

# get rid of extra index cols    
citizen = citizen[['lon', 'lat', 'common_name', 'obs_btm_trees', 'tree_type', 'entry_source']]
# export cleaned data; move on to next dataset
citizen.to_csv('data/citizen_clean.csv')

#### Combined Dataset ####
combined_df = pd.concat((bartlett, msfs, citizen))

# subset the columns that we want
combined_df = combined_df[['lon', 'lat', 'common_name', 'condition_class', 'tree_type', 'entry_source']]

# export combined data
combined_df.to_csv('data/btm_combined.csv')


