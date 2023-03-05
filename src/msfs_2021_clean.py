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

msfs_2021 = pd.read_csv('https://raw.githubusercontent.com/carriemn00/browntailmoth/main/data/msfs_raw.csv')
print(msfs_2021.shape)

# subset the columns that we want
msfs_2021 = msfs_2021[['Longitude', 'Latitude', 'Host', 'Count']]
# clean up col names
msfs_2021 = msfs_2021.rename(columns = {'Longitude': 'lon', 'Latitude': 'lat', 'Host': 'common_name', 
                              'Count': 'obs_btm'})

# add entry source col
msfs_2021.insert(4,'entry_source', np.full((msfs_2021.shape[0], 1), 'MSFS 2021'))

# add tree type col and copy over info from common_name col
msfs_2021.insert(3, 'tree_type', np.full((msfs_2021.shape[0], 1), np.nan))
msfs_2021['tree_type'] = msfs_2021.loc[:,'common_name'] 

# fill in tree_type col with appropriate values
msfs_2021['tree_type'] = msfs_2021['tree_type'].map({'Crabapple': 'Fruiting / Flowering', 
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

# ok! export data 
msfs_2021.to_csv('msfs_2021_clean.csv')