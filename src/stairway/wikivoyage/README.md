# Wikivoyage data pipeline

This README describes the different steps and utilities to extract and clean
the wikivoyage data set. 

## Structure

data_dir = `data/wikivoyage/`

1. parsing.py
    - goal: extracts content and metadata from raw xml.
    - input: `raw/enwikivoyage-20191001-pages-articles.xml.bz2`
    - output: `clean/wikivoyage_metadata_all.csv`
    - notebook: `parsing-wikivoyage.ipynb`
2. preprocessing.py
    - goal: cleans wikivoyage metadata.
    - input: `clean/wikivoyage_metadata_all.csv`
    - output: `processed/wikivoyage_destinations.csv`
    - notebook: `preprocessing-wikivoyage-metadata.ipynb`
3. feature_engineering.py
    - goal: adds features to the metadata.
    - input: `processed/wikivoyage_destinations.csv`
    - output: `enriched/wikivoyage_destinations.csv`
        - a copy is saved to the flak api directory (`api/data/`).
    - notebooks: 
        - `sampling-weight.ipynb`
        - `activities-bm25.ipynb`
            - input: `feature_terms.csv` and `feature_profiles.csv`
            - output: `enriched/wikivoyage_features.csv`
                - a copy is saved to the flak api directory (`api/data/`).
            - **TODO:** convert to module.
    
## Running the pipeline

**TODO:** Create a main.py that runs all above steps in one go.

For now, only the feature engineering pipeline can be run from the command line:

```bash
python src/stairway/wikivoyage/feature_engineering.py 
```

## API usage

A notebook named `flask-api-with-pandas.ipynb` demonstrates how the processed API
data is called in Flask.
