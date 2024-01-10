  

# CMPT 353 OSM Project

  

TODO: Update before project is submitted.

  

**Dependencies**

- Jupyter Notebook

- pandas

- numpy

- gmaps

- unidecode

- fuzzywuzzy

- scikit-learn

- scipy

- geopy

- matplotlib

- python-levenshtein

**Installation**

Anaconda or pip is reccommended to use as a package manager.

  

A simple `conda install` will work for all, except the following:

1. gmaps. Use `conda install -c conda-forge gmaps` or `pip install gmaps`.

2. fuzzywuzzy. Use `conda install -c conda-forge fuzzywuzzy` or `pip install fuzzywuzzy`

  

## **Running the code**

There are two notebooks to run: best-amenities.ipynb, and chains.ipynb. Both notebooks use amenities-vancouver.json.gz, which is identical to the file provided by Greg Baker (it's from the OSM data).

  

**Best Amenities**

Open with `jupyter-notebook best-amenities.ipynb`.

  

Produced files (note that **these files are already in the repository**, so you don't have to run anything to produce them):

- boundaries.csv. To produce the file, uncomment this line in best-amenities.ipynb: `# boundaries.to_csv('boundaries.csv')` and then run the cells. The comment should be at the bottom of cell 4 in the notebook (if not in cell 4, do ctrl-f to find it).

- records.csv. To produce the file, boundaries.csv must exist in the directory and run `python3 make-records.py`. *Creating the file will take about an hour,* depending on your computer. Note that to run the remaining cells in the notebook requires records.csv to exist.

  

**Chains vs. Non-Chains**

Open with `jupyter-notebook chains.ipynb`.

  

Produced files (note that **these files are already in the repository**, so you don't have to run anything to produce them):

- chains_restaurants.csv. Run all cells of the notebook to produce it.

- non_chain_restaurants.csv. Run all cells of the notebook to produce it.

  

Another thing to run: chains-analysis.py. 
Run with `python3 chains-analysis.py chain_restaurants.csv non_chain_restaurants.csv`


We do NOT recommend running this, as it will take many hours, but restaurantsByCity.py can be run with `python3 restaurantsByCity.py`, assuming
amenities-vancouver.json is located in the same directory. It produces restaurantsByCity.json, which is read by chains.ipynb
