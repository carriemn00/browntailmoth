#### Bartlett 2022 Data Cleaning
#### Carrie Nguyen
#### 2022-2023

# load libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci
plt.ioff()

bartlett_2022 = pd.read_csv('https://raw.githubusercontent.com/carriemn00/browntailmoth/main/data/points.csv')
print(bartlett_2022.shape)


# subset cols of interest
bartlett_2022 = bartlett_2022[['Longitude', 'Latitude', 'CommonName', 'ObservedBT',
                               'Dbh1', 'Condition']]

# insert col for entry source
bartlett_2022.insert(6,'entry_source', np.full((bartlett_2022.shape[0], 1), 'Bartlett 2022'))


# create common name col and copy over info from CommonName col
bartlett_2022.insert(3, 'common_name', np.full((bartlett_2022.shape[0], 1), np.nan))
bartlett_2022['common_name'] = bartlett_2022.loc[:,'CommonName'] 

# rename common_name col with shorter names (allows comparision with Citizen and MSFS data)
bartlett_2022 = bartlett_2022.replace({'common_name': {'Crabapple ' : 'Crabapple', 'Elm-American ' : 'Elm',
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

# insert col for tree type
bartlett_2022.insert(4, 'tree_type', np.full((bartlett_2022.shape[0], 1), np.nan))
# copy over info from common_name into tree type 
bartlett_2022['tree_type'] = bartlett_2022.loc[:,'common_name'] 
# fill in appropriate tree type based on common_name 
bartlett_2022['tree_type'] = bartlett_2022['tree_type'].map({'Crabapple': 'Fruiting / Flowering', 
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

# rename col names 
bartlett_2022 = bartlett_2022.rename(columns = {'Longitude': 'lon', 'Latitude': 'lat', 'CommonName': 'name', 'ObservedBT': 'obs_btm', 'Dbh1':'dbh1',
                                                'Condition': 'condition'})

# ok! export data 
bartlett_2022.to_csv('bartlett_2022_clean.csv')



