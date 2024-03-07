'''
this is the code to use the multispectrum camera using the raspberry pi
generic steps are as followed:
1. take picture
2. analyse picture
3. if fusarium is present than get the coordinates and store them in the list
4. once the drone has landed, filter the data
5. write the filtered data into a csv
6. terminate program
'''

def getCood():
    # Integrations
    # This function gets the coordinates using the gps module
    # returns: coordinates pair list -> [lat, long] -> [float, float]
    pass

def takePic():
    # Integration
    # This function takes the picture using the camera
    # returns: pic location -> string
    pass

def analyse():
    # AI
    # This function analyses the picture that was taken
    # returns: maybe coordinates pair list -> [lat, long] -> [float, float]
    pass

def connect():
    # Integration
    # This function connects to the camera
    # returns: bool
    pass

def writeCSV():
    # Integration
    # This function writes the coordinates into a csv.
    # returns: bool
    pass

def flightStatus():
    # Integration
    # This function checks wheather the code should run or not.
    # returns: bool
    pass

def createWindow():
    # Neel
    # This function will be used to create a window that has a "start" button
    # returns: bool
    pass

def filterData():
    # Neel/Integration
    # This function takes the raw data and filters it to the appropriately
    # returns: filted list of list -> [ [lat, long] ] -> [ [float, float] ]
    pass

def main():
    # All
    # main function
    # There should be a while loop for taking pictures and analysing them, 
    # once the loop is broken the data should be written in to a csv
    # returns: none
    pass

main()