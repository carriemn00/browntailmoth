# Brown-Tail Moth - Carrie Nguyen
clean_data:
	python -B src/browntail_data_cleaning.py
surveyor_plot:
	python -B src/surveyor_plot.py 
species_plot:
	python -B src/species_plot.py
tree_type_plot:
	python -B src/tree_type_plot.py

req:
	pip install -r requirements.txt
# Download the data
# mkdir -p fails quietly if directory already exists
# curl -L follows indirects
# curl -O preserves filename of source
data:
	mkdir -p data
	cd data; curl -LO https://raw.githubusercontent.com/carriemn00/browntailmoth/main/data/bartlett_raw.csv?token=GHSAT0AAAAAABZAOY6OI6Y5UIYSAZAT4GT6Y4Y26JQ
	cd data; curl -LO https://raw.githubusercontent.com/carriemn00/browntailmoth/main/data/msfs_raw.csv?token=GHSAT0AAAAAABZAOY6O72AAJAMV2R6E5C3UY4Y3DAA
	cd data; curl -LO https://raw.githubusercontent.com/carriemn00/browntailmoth/main/data/citizen_raw.csv?token=GHSAT0AAAAAABZAOY6O65F4M5DPXCH7JOMKY4Y27FA
	cd data; curl -LO https://github.com/carriemn00/browntailmoth/blob/main/data/Maine_Town_and_Townships_Boundary_Polygons_Feature.zip
	mkdir -p figs

clean:
	rm -rf data