'''
This is a coordinate class stores coordinates at a certain location

The latitude and longtitude can be accessed using wayPoints function that returns two values: latitude and longtitude
'''
class Coordinate():
    def __init__(self, lat=0, lon=0):
        self.lat = lat
        self.lon = lon
    
    def setPoint(self, newLat, newLon):
        self.lat = newLat
        self.lon = newLon

    def wayPoints(self):
        return float(self.lat), float(self.lon) 
    
    def lat(self):
        return float(self.lat)

    def lon(self):
        return float(self.lon)
   
    def __str__(self) -> str:
        out = "Coordinates are: " + "{:.6f}".format(self.lat) + " " + "{:.6f}".format(self.lon)
        return out
    
