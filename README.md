# VATTS - Virtual Assistant for Travel Time Schedule 
VATTS is an itinerary generating system, for travelers who prefer an
organized trip but with less time and effort spent on doing research and scheduling. 


## Usage
Main server is based on flask. To run the server:
```python flask_main.py```
### API key
The server needs a Google API key to run. The API key should have google place API and google map web API enabled.   
You will need to add you key to `API_KEY.py` and `webpage\page2.html`

## Data Script
Our data is from google API and Yelp fusion API. In the `/Get_data` Directory, `script.py` was used to acquire the detail of POI, `route_script.py` was used to acquire the distance between any two POI.

## Data Clean Script
The data is located in `CSE6242/Data_Clean/Data_Cleaned/data_with_types`, the coresponding cleaning script is `CSE6242/Data_Clean/Data_Clean_json_with_types.py`.

The `formatted_Google_Attraction_*` looks like this:

| name | formatted_address | rating | types | lat | lng | id | place_id |  
| ---: | ----------------: | -----: | ----: | --: | --: | -: | -------: |


We can use the rating as a weight, which should be discussed later.

## Dependencies
### Python Version
`pythone 3.7` is used to construct and test this project. We haven't tested it on any other version.  
### External Library
`Click 7.0`   
`Flask 1.0.2`  
`Jinja2 2.10`  
`MarkupSafe 1.1.0`  
`Werkzeug 0.14.1`  
`certifi 2018.11.29`  
`chardet 3.0.4`  
`idna 2.7`  
`itsdangerous 1.1.0`  
`numpy 1.15.4`  
`pandas 0.23.4`  
`pytz 2018.7`  
`requests 2.20.1`  
`scipy 1.1.0`  
`six 1.11.0`  
`urllib3 1.24.1`  
#### Quick install
Refer to `requirement.txt` and used `pip` to install all dependencies at once. 
 




##