# Get Closest Food Trucks

## Usage

```
python3 main.py  
```

## API

`GET /close`
```
curl --request GET 'http://127.0.0.1:5000/close?lat=37.78021548028814&lng=-122.41602577015111&num=2'
```
Params
```
lat: Latitude 
lng: Longitude
num: Number of Closest Trucks
```
Response
```
{
            "status":"success",
            "payload":{
                "type": "FeatureCollection", 
                "features":[...]
            }
}
```

`GET /trucks`
```
curl --request GET 'http://127.0.0.1:5000/trucks?pp=10&pn=1'
```
Params
```
pp: Items Per Page 
pn: Page Number
```

Response
```
{
            "status":"success",
            "payload":{
                "tc":"455",
                "data:{ 
                    "type": "FeatureCollection", 
                    "features":[...]
                }
            }
}
```

## Description
The API is built with [Flask]("https://flask.palletsprojects.com/en/2.1.x/).

The API fetches and processes data from a local file in the same directory. In this implementation the file is 
> sanfransiscofoodtruckdata.json

The API use [GeoPandas]("https://geopandas.org/en/stable/") to process and serve the data. The important part of data processing is in projecting the location data to appropriate coordinate system so that the distances can be easily calculated.

The API employs caching using [Flask-Cache]("https://pythonhosted.org/Flask-Cache/). The requests are cached and function `data_get_closest_truck` which calculates and finds the closest truck to any given location is memoized.

## Future
The API can be easily scalled by projecting the new data points properly and attaching any external database.