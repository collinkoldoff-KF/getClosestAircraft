import urllib3
import os
import requests
import json
from math import sin, cos, sqrt, atan2, radians, pi
try:
    from coords import myLat, myLng, amountToPrint, degRange
except:
    f = open("coords.py", "w")
    f.write("myLat = 37.3735\nmyLng = -92.4737\ndegRange = 1\namountToPrint = 3")
    f.close()
    from coords import myLat, myLng, amountToPrint, degRange

if os.path.exists("coords.py") == False:
    input()

def getDistance(x1, x2, y1, y2):

    #φ is latitude, λ is longitude
    R = 6371e3; #metres
    φ1 = x1 * pi/180; #φ, λ in radians
    φ2 = x2 * pi/180;
    Δφ = (x2-x1) * pi/180;
    Δλ = (y2-y1) * pi/180;

    a = sin(Δφ/2) * sin(Δφ/2) + cos(φ1) * cos(φ2) * sin(Δλ/2) * sin(Δλ/2);
    c = 2 * atan2(sqrt(a), sqrt(1-a));

    d = R * c; #in metres

    return d

boundsUpperLat = myLat + degRange
boundsUpperLng = myLng - degRange

boundsLowerLat = myLat - degRange
boundsLowerLng = myLng + degRange

# http://data-live.flightradar24.com/zones/fcgi/feed.js?bounds=37.3612,47.3612,-84.0261,-94.0261&adsb=1&air=1&array=1

endpoint = f"https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds={boundsUpperLat},{boundsLowerLat},{boundsUpperLng},{boundsLowerLng}&air=1"

response = requests.get(endpoint, headers={'User-Agent':"helloThere"})
jsonData = json.loads(response.text)
del jsonData['full_count'],jsonData['version']

aircrafts = jsonData.keys()

for aircraft in aircrafts:
    aircraftData = jsonData[aircraft]
    distance = getDistance(myLat, float(aircraftData[1]), myLng, float(aircraftData[2]))
    aircraftData.append(round(distance/1852,3))
    if aircraftData[5] == "":
        aircraftData[5] = "N/A"
    if aircraftData[9] == "":
        aircraftData[9] = "N/A"
    if aircraftData[8] == "":
        aircraftData[8] = "N/A"
    if aircraftData[16] == "":
        aircraftData[16] = "N/A"
    if aircraftData[11] == "":
        aircraftData[11] = "N/A"
    if aircraftData[12] == "":
        aircraftData[12] = "N/A"
    try:
        aircraftDatas.append(aircraftData)
    except:
        aircraftDatas = [aircraftData]

aircraftDatas.sort(key = lambda aircraftDatas: aircraftDatas[19])

i1 = 1
for item in aircraftDatas:
    item.append(i1)
    i1+=1

i2 = 0
for closestAcft in aircraftDatas:
    if i2 == 0:
        try:
            print(f"{closestAcft[20]}: Callsign: {closestAcft[16]}, Type: {closestAcft[8]}, Reg: {closestAcft[9]}, Altitude: {closestAcft[4]}, Ground Speed: {closestAcft[5]}, Route: {closestAcft[11]}-{closestAcft[12]}, Distance(nm): {closestAcft[19]}")
            print("\n")
        except:
            print("None")
            break
    elif i2 != amountToPrint:
        try:
            print(f"{closestAcft[20]}: Callsign: {closestAcft[16]}, Type: {closestAcft[8]}, Reg: {closestAcft[9]}, Altitude: {closestAcft[4]}, Ground Speed: {closestAcft[5]}, Route: {closestAcft[11]}-{closestAcft[12]}, Distance(nm): {closestAcft[19]}")
        except:
            break
    elif i2 == amountToPrint:
        break
    i2+=1