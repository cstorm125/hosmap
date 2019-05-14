# hosmap
Nearest Hospital Contour Map based on Time Traveled for Thailand

## Getting Started

Have you ever wondered if you had a stroke in the middle of the night, would you be able to get to the hospital in time? Wonder no more. [hosmap](https://api.mapbox.com/styles/v1/pnphannisa/cjn1335a14z3g2rsehvs818j3.html?fresh=true&title=true&access_token=pk.eyJ1IjoicG5waGFubmlzYSIsImEiOiJjaXVvamFoeTcwMWhjMnRtMWRmeXczZG4yIn0.LjKO5l7YlXgRApgB-jssUg#9/13.8475/100.6639) is a nearest hospital contour map based on time traveled by car for all of Thailand.

See full report at our [Medium](https://medium.com/@iwishcognitivedissonance/this-map-shows-if-you-will-get-to-the-hospital-in-time-from-anywhere-in-thailand-fd73d13aa3db).

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

## ตัวแปรที่น่าสนใจเพื่อ Thailand ICT Camp 2019

```
year.year
[1] 2008 2009 2010 2011 2012 2013 2014 2015

$time.time
 [1] "12011300 " "21012200 " "16011700 " "14011500 " "13011400 " "15011600 "
 [7] "24010100 " "22012300 " "02010300 " "08010900 " "23012400 " "09011000 "
[13] ""          "05010600 " "01010200 " "11011200 " "20012100 " "10011100 "
[19] "07010800 " "19012000 " "06010700 " "18011900 " "04010500 " "17011800 "
[25] "03010400 "

$belt.belt
[1] "เข็มขัด"  "ใส่หมวก" "ไม่ใส่"  

$drinking.drinking
[1] "ไม่ดื่ม" "ดื่ม"  

$sex.sex
[1] "หญิง" "ชาย"

$location.location
[1] "ในเมือง"  "ทางหลวง" "ไม่ทราบ"  "ชนบท"   

$patient_status.patient_status
[1] "ผู้ชับขี่"     "ผู้โดยสาร"  "คนเดินเท้า" "ไม่ทราบ"  

$vehicle_1.vehicle_1
 [1] "รถเก๋ง/แท็กซี่"    "จักรยานยนต์"     "อื่นๆ"           "ไม่ทราบ"        "รถจักรยาน"     
 [6] "สามล้อถีบ"       "ไม่มี/ล้มเอง"     "สามล้อเครื่อง"    "ปิคอัพ"          "รถโดยสารใหญ่"  
[11] "รถตู้"           "รถโดยสาร 4 ล้อ" "รถบรรทุก"      

$vehicle_2.vehicle_2
 [1] "ไม่มี/ล้มเอง"     "รถตู้"           "จักรยานยนต์"     "ปิคอัพ"          "รถเก๋ง/แท็กซี่"   
 [6] "สามล้อถีบ"       "รถจักรยาน"      "ไม่ทราบ"        "รถโดยสาร 4 ล้อ" "สามล้อเครื่อง"   
[11] "รถโดยสารใหญ่"   "อื่นๆ"           "รถบรรทุก"      

$age.age
 [1] 54 13 59 41 42 26 21 31 28 22 20 39 58 44 33 30 32 17 23 18 19 36  3  2 38 34 64
[28] 88 50 27  6 40 43 45 48 47 25 24 16 35  9 10 12 29 46 56 61 15 14 60 51 52 62 87
[55] 55  4  5 57 70 37 49 11  7  1 53 71  8 78 63 66 67 68 65 69 84 98 74 73 72 77 85
[82] 82 83 79 76 75 92 81 96 80 93 86 89 90 97 91 94 95

$reporter.reporter
[1] "ผู้ประสบเหตุ/ญาติ" "มูลนิธิ/อาสาสมัคร" "เจ้าหน้าที่ตำรวจ"  "ไม่นำส่ง"        "BLS"          
[6] "ALS"           "FR"            "เสียชีวิตที่เกิดเหตุ" "ILS"          

$province.province
 [1] "กรุงเทพมหานคร"  "สมุทรปราการ"    "นนทบุรี"         "ปทุมธานี"        "พระนครศรีอยุธยา"
 [6] "อ่างทอง"        "ลพบุรี"          "สิงห์บุรี"         "ชัยนาท"         "สระบุรี"        
[11] "ชลบุรี"          "ระยอง"         "จันทบุรี"         "ตราด"          "ฉะเชิงเทรา"    
[16] "ปราจีนบุรี"       "นครนายก"       "สระแก้ว"        "นครราชสีมา"     "บุรีรัมย์"        
[21] "สุรินทร์"         "ศรีสะเกษ"       "อุบลราชธานี"     "ยโสธร"         "ชัยภูมิ"         
[26] "อำนาจเจริญ"     "หนองบัวลำภู"     "ขอนแก่น"        "อุดรธานี"        "เลย"          
[31] "หนองคาย"       "มหาสารคาม"     "ร้อยเอ็ด"        "กาฬสินธุ์"        "สกลนคร"       
[36] "นครพนม"        "มุกดาหาร"       "เชียงใหม่"       "ลำพูน"          "ลำปาง"        
[41] "อุตรดิตถ์"        "แพร่"           "น่าน"           "พะเยา"         "เชียงราย"      
[46] "แม่ฮ่องสอน"      "นครสวรรค์"      "อุทัยธานี"        "กำแพงเพชร"     "ตาก"          
[51] "สุโขทัย"         "พิษณุโลก"        "พิจิตร"          "เพชรบูรณ์"       "ราชบุรี"        
[56] "กาญจนบุรี"       "สุพรรณบุรี"       "นครปฐม"        "สมุทรสาคร"      "สมุทรสงคราม"   
[61] "เพชรบุรี"        "ประจวบคีรีขันธ์"   "นครศรีธรรมราช"  "กระบี่"          "พังงา"         
[66] "ภูเก็ต"          "สุราษฎร์ธานี"     "ระนอง"         "ชุมพร"          "สงขลา"        
[71] "สตูล"           "ตรัง"           "พัทลุง"          "ปัตตานี"         "ยะลา"         
[76] "นราธิวาส"       "บึงกาฬ"        

$referral_flag.referral_flag
[1] "ไม่"            "admit"         "ส่งต่อก่อน admit" "ส่งต่อหลัง admit"
```
