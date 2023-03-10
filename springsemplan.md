# Spring 2023
### Carrie Nguyen

- New dataset from 2022! (Public lands only)
## Visualization
- Indicate Public vs Private lands
- Color by Deciduous Trees
### GIS
- Obtain high quality GIS maps of Waterville area light pollution (NASA; https://www.msgc.org/students/) and leaf-off forest density (NAIP - leaf-off map of Waterville (also GoogleEarth))
  - Calculate population index based on these measures
- ARCGIS image classifier 
  - Use classifier to create layer stack of leaf off and leaf on (deciduous forests and evergreen forests)
- Quantification - Index (Outbreak Density, Proximity to light, Deciduous canopy cover)
- Compare BTM density and forestry data with historical BTM and forestry data
- Interactive visualizations

## Survey
- Implement standardized set of questions for coming year of surveys
  - **Counts of BTM nests**

# Schedule
**2/5:**
- Preliminary meeting
- Set up GIS meeting with Manny

**2/12:**
- Meeting with Tahiya
- Read light pollution paper
- Begin GIS tutorials

**2/19:**
- 2/21: Completed 3 GIS tutorials
- Add new datasets to visualizations
- Determine if any regression/ analyses can be performed at this stage
**2/26:**
- Finish up GIS tutorials
- Uploading datasets to GIS map
  - 4 datasets now
  - 3 have BTM nest counts (Citizen does not)

**3/5:**
- Point Density analyses for quantifying areas of BTM infestation (weights by BTM counts); do this only for datasets we have nest info for
  - `Population field = obs_btm`
  -  `Output cell size = 10`
  -  `Radius = 300 sq meters`
  -  Remember to set `Output Coordinates` to `NAD 1983` and set the `extent` and `mask` to `Waterville_boundary`!

**3/12:**

**3/19:**

**3/26:**

**4/2:**

**4/9:**

**4/16:**
- Finalize CLAS presentation materials

**4/23:**
- CLAS presentation

**4/30:**

**5/7:**
