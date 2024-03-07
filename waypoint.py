import coordinate

# this class is a container to hold the coordinates for the path of the flight
class WaypointCont():
    def __init__(self):
        self.path = []
        self.topLeft = coordinate.Coordinate()
        self.topRight = coordinate.Coordinate()
        self.bottomLeft = coordinate.Coordinate()
        self.bottomRight = coordinate.Coordinate()
        self.x_disp = 0.00001
        self.y_disp = 0.00002
        self.totalDistance = 0

    def addWayPoint(self, coor):
        self.path.append(coor)

    def setTopLeft(self, lat, lon):
        self.topLeft.setPoint(lat, lon)
        print("Top left set to:" , self.topLeft.lat, self.topLeft.lon)
    
    def setTopRight(self, lat, lon):
        self.topRight.setPoint(lat, lon)
        print("Top right set to:" , self.topRight.lat, self.topRight.lon)

    def setBottomLeft(self, lat, lon):
        self.bottomLeft.setPoint(lat, lon)
        print("Botom left set to:" , self.bottomLeft.lat, self.bottomLeft.lon)

    def setBottomRight(self, lat, lon):
        self.bottomRight.setPoint(lat, lon)
        print("Bottom right set to:" , self.bottomRight.lat, self.bottomRight.lon)
    
    def set_x_disp(self, x):
        self.x_disp = x

    def set_y_disp(self, y):
        self.y_disp = y

    def indexCoor (self, i):
        if (i >= len(self.path)):
            return 0,0
        else:
            return self.path[i].lat, self.path[i].lon

    # todo: turn float numbers into integers, create loop from top left to bottom 
    # right (while loops), then convert back to float and create new coordinate for
    # new point 
    def createFlightPath(self):
        print("\nCreating Path...")
        topLeftLAT, topLeftLON = self.topLeft.wayPoints()
        bottomRightLAT, bottomRightLON = self.bottomRight.wayPoints()

        # number of x and y steps needed (convert to int to be used in for loop)
        num_x_steps = abs(int((bottomRightLAT - topLeftLAT) / self.x_disp))
        num_y_steps = abs(int((bottomRightLON - topLeftLON) / self.y_disp))

        print("x-steps:", num_x_steps, "and y-steps:", num_y_steps)

        # Move horizontally from the top left to the top right
        for x in range(num_x_steps + 1):
            self.path.append(coordinate.Coordinate(topLeftLAT + x * self.x_disp, topLeftLON))
            self.totalDistance+= 1.11

        # Move down a certain y-distance
        topLeftLAT, topLeftLON = topLeftLAT, topLeftLON - self.y_disp
        self.totalDistance += self.y_disp

        # Alternate direction of movement in x-direction until the bottom right is reached
        for y in range(num_y_steps):
            if y % 2 == 0:
                for x in range(num_x_steps, -1, -1):
                    self.path.append(coordinate.Coordinate(topLeftLAT + x * self.x_disp, topLeftLON - y * self.y_disp))
                    self.totalDistance+= 1.11
            else:
                for x in range(num_x_steps + 1):
                    self.path.append(coordinate.Coordinate(topLeftLAT + x * self.x_disp, topLeftLON - y * self.y_disp))
                    self.totalDistance+= 1.11
            self.totalDistance-= 2*1.11


    def pathWay(self):
        if len(self.path) == 0:
            print("No points have been entered and processed.")
        else:
            return self.path
        
    def printPathway(self):
        for i in self.path:
            print(i)
        print("Total Points:", len(self.path))
        print("Total distance is:", (self.totalDistance), "m")