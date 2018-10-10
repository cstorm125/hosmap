# hosmap
Nearest Hospital Contour Map based on Time Traveled for Thailand

## Getting Started

Have you ever wondered if you had a stroke in the middle of the night, would you be able to get to the hospital in time? Wonder no more. [hosmap](https://api.mapbox.com/styles/v1/pnphannisa/cjn1335a14z3g2rsehvs818j3.html?fresh=true&title=true&access_token=pk.eyJ1IjoicG5waGFubmlzYSIsImEiOiJjaXVvamFoeTcwMWhjMnRtMWRmeXczZG4yIn0.LjKO5l7YlXgRApgB-jssUg#9/13.8475/100.6639) is a nearest hospital contour map based on time traveled by car for all of Thailand.

See full report at our [Medium]().

## Mapping Procedures

1. Retrieve hospital physical addresses from 26,881 hospitals listed by [Ministry of Public Health](http://203.157.10.8/hcode_2014/p_export.php?p=3), downloaded as `hospital_addresses.csv`.
2. Augment the data with latitude and longitude using [Google Map API](https://cloud.google.com/maps-platform/), resulting in `hospital_latlon.csv`. Scraping script can be found at `scripts/scrape_geocode.py`. More detailed data manipulations can be found in `notebooks/codebook.html`
3. Use ArcGIS to cast 1X1 km fishnets as proxies of all locations in Thailand
```
Data Management Toolbox > Sampling Toolset > Create Fishnet
Cell Width: 1,000 m
Cell Height: 1,000 m
The output is a vector location fishnet.
```
4. Use ArcGIS to find the shortest Euclidean distance between all points to their respective nearest hospitals. This is not ideal since nearest hospitals could be different from nearest Euclidean hospitals in some edge cases but it is a necessary step to save computational power.
```
Analysis toolbox > Proximity toolset > Near
In_cover: location fishnet
Near_cover: locations of hospitals
Feature_type: POINT
Search radius: 200 km (to limit number of calculation)
Location: LOCATION (to return geographic coordinates of the shortest location)
The output is a vector location fishnet with a NEAR column which indicates the shortest Euclidean distance in meters, and latitude and longitude of the nearest hospital.
```
5. Use [Graphhopper API](https://graphhopper.com/api/1/docs/routing/) to calculate travel distance and travel time by car from any point to its nearest hospital (about 500,000 points) and saved file as `route_hos_all.csv`. See `scripts/graphhopper_api.py` for more details.
6. Use ArcGIS to plot travel time fishnet and create a Digital Elevation Model (DEM) of 'travel time by car to the nearest hospital' layer.
```
3D Analyst Toolbox > Raster Interpolation Toolset > Topo to Raster
Input layer: location fishnet layer with data of shortest travel distance and time
Field: Travel ime
Type: POINTELEVATION
Cell size: 1 km, 1 km
The output is a raster DEM layer of the of 'travel time by car to the nearest hospital'.
```
7. Use ArcGIS to convert raster DEM -> vector polyline layer of 'travel time by car to the nearest hospital' of 10-minute interval between each contour line.
```
3D Analyst Toolbox > Raster Surface Toolset > Contour
In_raster: travel time DEM layer
Contour interval: 10 minutes
Contour type: CONTOUR
The output is a vector polyline layer with a CONTOUR column which indicates the travel time by car to the nearest hospital of each lines.
```
8. Visualize 'travel time by car to the nearest hospital' (polyline) and locations of hospitals by [Mapbox](https://www.mapbox.com/).
```
Template: light
Uploaded additional layers: hospital locations (points), and travel time contour (polylines)
Hospital locations: visualized by hospital icon, size adjusted for each zoom level
Travel time contour: visualized by graduated color of travel time, 9 classes (0, 10, 20, 30, 40, 60, 90, 140, and greater minutes), line thickness adjusted for each zoom level
Travel time label (showing travel time in text in addition to the contour): duplicated from travel time contour, font size adjusted for each zoom level
```
