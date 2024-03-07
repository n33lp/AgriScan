"""
This is the actual program that we would use to connect our drone, take-off, give it coordiantes, and land
"""

from dronekit import connect, VehicleMode, LocationGlobalRelative
# from pymavlink import mavutil
import time
import argparse 
import waypoint
import coordinate
import csv
import colour_detection
 
parser = argparse.ArgumentParser()
parser.add_argument('--connect', default='127.0.0.1:14550')    
args = parser.parse_args()



# Function to arm and then takeoff to a user specified altitude
# parameter: target altitude that drone would reach to consider "complete" takeoff
def arm_and_takeoff(aTargetAltitude):

  print ("Basic pre-arm checks")
  # Don't let the user try to arm until autopilot is ready
  while not vehicle.is_armable:
    print (" Waiting for vehicle to initialise...")
    time.sleep(1)
        
  print ("Arming motors")
  # Copter should arm in GUIDED mode
  vehicle.mode    = VehicleMode("GUIDED")
  vehicle.armed   = True

  while not vehicle.armed:
    print (" Waiting for arming...")
    time.sleep(1)

  print ("Taking off!")
  vehicle.simple_takeoff(aTargetAltitude) # Take off to target altitude

  # Check that vehicle has reached takeoff altitude
  while True:
    print (" Altitude: ", vehicle.location.global_relative_frame.alt) 
    #Break and return from function just below target altitude.        
    if vehicle.location.global_relative_frame.alt>=aTargetAltitude*0.95: 
      print ("Reached target altitude")
      break
    time.sleep(1)

    
##This function ensures that the vehicle has landed (before vechile.close is called)
def Land():
  print("Landing")
  ##thread_distance.join()
  time.sleep(1)
  vehicle.mode = VehicleMode("LAND")
  while vehicle.armed:
    time.sleep(1)
  vehicle.close()

# Function: will take four corner input from top left, top right, bottom left, bottom right
#           and store them as list Coordinate with lat and lon
# Parameter: None
# Return: list of cooridnates of four corners
def pathInputs():
  corners = ["top left", "top right", "bottom left", "bottom right"]
  coordinates = []
  for corner in corners:
    lat, lon = input('Enter latitude and longitude of '+ corner + ': ').split()
    coordinates.append(coordinate.Coordinate(lat,lon))
  return coordinates

# Function: will take four corner and return path of all the different waypoints from top left
#           to bottom right in lawnmower pattern
# Parameter: coordinates of corners
# Return: waypoint object with coordonates of path that drone takes
def createPath(coordinates):
  print("Creating Path...")
  path = waypoint.WaypointCont()
  path.setTopLeft(coordinates[0].lat, coordinates[0].lon)
  path.setTopRight(coordinates[1].lat, coordinates[1].lon)
  path.setBottomLeft(coordinates[2].lat, coordinates[2].lon)
  path.setBottomRight(coordinates[3].lat, coordinates[3].lon)
  path.createFlightPath()
  return path

#----begin programming form here----------------------------------------------------------#

altitude = 10
airspeed = 1
numOfDigits = 6
prevLat = 0
prevLon = 0
arrFungalPresence = []

# Connect to the Vehicle
print ('Connecting to vehicle on: %s' % args.connect)
vehicle = connect(args.connect, baud=57600, wait_ready=True)

arm_and_takeoff(altitude) ##------------ arm and reach 20m alt 

vehicle.airspeed = airspeed ##set speed that drone goes at

coordinates = pathInputs() # gets four corners
path = createPath(coordinates) # creates lawnmower pattern for drone to fly over

# drone will got the the coordinates in path
with open("coordinates.csv", "w") as coorfile:
  filewriter = csv.writer(coorfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
  filewriter.writerow(['Latititude', 'Longtitude'])
  for wp in path.path:
    nextCoor = LocationGlobalRelative(wp.lat, wp.lon, altitude)
    vehicle.simple_goto(nextCoor)
    
    # fluorescence detection
    infectionDetected = colour_detection.pink_identify()
    
    # if fluorescence detected and coordinates are not the same as previous coordinates, then will add to csv
    if infectionDetected:
      if(round(wp.lat, numOfDigits-1) != prevLat and round(wp.lon, numOfDigits - 1) != prevLon):
        arrFungalPresence.append(wp)
        prevLat = round(wp.lat, numOfDigits - 1)
        prevLon = round(wp.lon, numOfDigits - 1)
        filewriter.writerow([prevLat, prevLon])
    
# drone flies back to original position
lastCoor  =  LocationGlobalRelative(path.path[0].lat, path.path[0].lon, altitude)
vehicle.simple_goto(lastCoor)
time.sleep(5)

# landing function
Land()
