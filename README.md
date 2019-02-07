# Property Search API Overview

## 1. Purpose

This API is used to return the results on the basis of user's search params.

## How It Works
This takes the 8 parameters and uses post request method and return an array of JSON Object

**List of params are**
lat, lon, min_budget,max_budget,min_bedrooms,max_bedrooms,min_bathrooms,max_bathrooms
**Returns**
array of JSON Objects with following keys:
property_name, price, no_of_bedrooms, no_of_bathrooms,city,match_score,distance_from_user

## Tech Stack
Backend - python, django, postgres, elasticsearch, requsts library.
FrontEnd - Angular5

## Explaination of logic
1. In elastic search, I created index called property_search, check elatic.py

2. I wrote post_save signal, Data get indexed in elasticsearch index when end user adds any properties in database. for ref: check models.py

3. I'm using geopoint datatype to query lat lon in elasticsearch, check get_elastic_query method utils.py.

