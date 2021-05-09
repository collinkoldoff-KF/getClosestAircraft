import urllib3
import os
from math import sin, cos, sqrt, atan2, radians
try:
    from coords import myLat, myLng
except:
    f = open("coords.py", "w")
    f.write("myLat = 37.3735 \nmyLng = -92.4737")
    f.close()
    from coords import myLat, myLng

if os.path.exists("coords.py") == False:
    input()

# this is incorrect because longitude changes distance
def getDistance(x1, x2, y1, y2):

    d = sqrt(pow(x2 - x1, 2) + pow(y2 - y1, 2))

    return d

boundsUpperLat = myLat + 5
boundsUpperLng = myLng - 5

boundsLowerLat = myLat - 5
boundsLowerLng = myLng + 5

# http://data-live.flightradar24.com/zones/fcgi/feed.js?bounds=37.3612,47.3612,-84.0261,-94.0261&adsb=1&air=1&array=1

endpoint = f"https://data-live.flightradar24.com/zones/fcgi/feed.js?bounds={boundsUpperLat},{boundsLowerLat},{boundsUpperLng},{boundsUpperLng}&air=1"


prevDist = -1
closestAcft = "None"

data = str(urllib3.PoolManager().request('GET', endpoint).data).split("\\n,")
data.pop(0)

for line in data:
    try:
        acft = line.split(":")[1].strip("[]").replace("\"", "").split(",")
        distance = getDistance(myLat, float(acft[1]), myLng, float(acft[2]))
        if prevDist != -1 and distance < prevDist:
            prevDist = distance
            closestAcft = acft
        elif prevDist == -1:
            prevDist = distance
            closestAcft = acft
    except:
        pass

print(f"Callsign {closestAcft[16]}, Type {closestAcft[8]}, Reg {closestAcft[9]}, Altitude {closestAcft[4]}, Ground Speed {closestAcft[5]}, {closestAcft[11]}-{closestAcft[12]}")
input("Press Any Key To Continue...")