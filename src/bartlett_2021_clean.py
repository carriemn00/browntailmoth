#### Bartlett 2021 Data Cleaning
#### Carrie Nguyen
#### 2022-2023

# load libraries
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as sci
plt.ioff()

# read in data
bartlett_2021 = pd.read_csv('https://raw.githubusercontent.com/carriemn00/browntailmoth/main/data/bartlett_raw.csv')
print(bartlett_2021.shape)

# subset cols of interest
bartlett_2021 = bartlett_2021[['Longitude', 'Latitude', 'Common Name', 
                               'Tree Type (Ornamental | Fruiting / Flowering | Bush)',
                               'ObservedBTMNests','Dbh 1', 'Condition Class']]

# rename cols
bartlett_2021 = bartlett_2021.rename(columns = {'Longitude': 'lon', 'Latitude': 'lat', 'Common Name': 'name', 'ObservedBTMNests': 'obs_btm', 
                                                'Dbh 1':'dbh1', 'Tree Type (Ornamental | Fruiting / Flowering | Bush)': 'tree_type',
                                                'Condition Class': 'condition'})

# insert col for entry source
bartlett_2021.insert(7,'entry_source', np.full((bartlett_2021.shape[0], 1), 'Bartlett 2021'))

# create common name col and copy over info from name col
bartlett_2021.insert(3, 'common_name', np.full((bartlett_2021.shape[0], 1), np.nan))
bartlett_2021['common_name'] = bartlett_2021.loc[:,'name'] 

# rename common_name col with shorter names (allows comparision with Citizen and MSFS data)
bartlett_2021 = bartlett_2021.replace({'common_name': {'Crabapple ' : 'Crabapple', 'Elm-American ' : 'Elm',
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

# ok! export data 
bartlett_2021.to_csv('bartlett_2021_clean.csv')
