"""
This is a test file that was copied from https://dronekit-python.readthedocs.io/en/latest/guide/quick_start.html
to test the conditions of a test drone.
"""

print("Start simulator (SITL)")
import dronekit_sitl
import coordinate
import waypoint
import coordinate
# Import DroneKit-Python
from dronekit import connect, VehicleMode, LocationGlobalRelative

import time
import colour_detection
sitl = dronekit_sitl.start_default()
connection_string = sitl.connection_string()

# takeoff
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

# Connect to the Vehicle.
print("Connecting to vehicle on: %s" % (connection_string,))
vehicle = connect(connection_string, wait_ready=True)

# Get some vehicle attributes (state)
print("Get some vehicle attribute values:")
print(" GPS: %s" % vehicle.gps_0)
print(" Battery: %s" % vehicle.battery)
print(" Last Heartbeat: %s" % vehicle.last_heartbeat)
print(" Is Armable?: %s" % vehicle.is_armable)
print(" System status: %s" % vehicle.system_status.state)
print(" Mode: %s" % vehicle.mode.name)    # settable

# add simulation path
altitude = 10

arm_and_takeoff(altitude)

vehicle.airspeed = 1 ##set speed that drone goes at

coordinates = pathInputs() # gets four corners
path = createPath(coordinates) # creates lawnmower pattern for drone to fly over

# drone will got the the coordinates in path
for wp in path.path:
    nextCoor = LocationGlobalRelative(wp.lat, wp.lon, altitude)
    vehicle.simple_goto(nextCoor)
    if colour_detection.pink_identify_sim == 1:
      print("Fluorescence Detected at: (" + wp.lat + ", " + wp.lon + ")")
    
    
lastCoor  =  LocationGlobalRelative(path.path[0].lat, path.path[0].lon, altitude)
vehicle.simple_goto(lastCoor)

# Close vehicle object before exiting script
vehicle.close()

# Shut down simulator
sitl.stop()
