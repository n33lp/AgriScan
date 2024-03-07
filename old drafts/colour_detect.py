#https://www.youtube.com/watch?v=cMJwqxskyek&ab_channel=CreepyD
#https://raspberrypi-guide.github.io/programming/install-opencv - for installing opencv
#https://sparklers-the-makers.github.io/blog/robotics/use-neo-6m-module-with-raspberry-pi/ 

# install for opencv
# sudo apt-get update
# sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
# pip install opencv-python==4.5.3.56

# all the installs
'''
sudo apt-get update && sudo apt-get -y 
install gpsd gpsd-clients python-gps
sudo shutdown -r now
sudo dpkg-reconfigure gpsd
sudo nano /etc/default/gpsd

in gpsd file, change config to:
START_DAEMON="true"
USBAUTO="true"
DEVICES="/dev/ttyACM0"
GPSD_OPTIONS="/dev/ttyACM0"
'''

# installs to read gps coordinates from gpsd_options
'''
pip install pynmea2

might also need to disable serial ports using:
1. (if serial0 conencted to ttyAMA0)
sudo systemctl stop serial-getty@ttyAMA0.service
sudo systemctl disable serial-getty@ttyAMA0.service

or 

2. (is serial0 connected to ttyS0)
sudo systemctl stop serial-getty@ttyS0.service
sudo systemctl disable serial-getty@ttyS0.service
'''

# 1 degree = 111320 m

# Importing all modules
import cv2
import numpy as np
import csv

# imports for reading gps coordinates
import serial
import time
import string
import pynmea2


# Specifying upper and lower ranges of color to detect in hsv format

# startLat = 0
# startLon = 0
# currentLat= 0
# currentLon = 0

port="/dev/ttyACM0" # port which GPS module is connected to

"""
method: reads data from usb port that has GPS module and returns the latitude and longitude
param: none
return: latitude and longitude
"""
def readGPSCoordinate():
    while True:
        # reads from port
        ser=serial.Serial(port, baudrate=9600, timeout=0.5)
        dataout = pynmea2.NMEAStreamReader()
        newdata=ser.readline().decode().strip()    

        # retrieves GPS coordinates and parses it to get float values for latitude and longitude
        if newdata[0:6] == "$GPRMC":
            newmsg=pynmea2.parse(newdata)
            lat=newmsg.latitude
            lon=newmsg.longitude
            break
    return lat,lon

def main():
    lower = np.array([40, 150, 20])
    upper = np.array([70, 255, 255]) # (These ranges will detect pink)
    minStartDistance = 0.00001 # 0.00001 degree = 1.11320 m
    numOfDigits = 6
    prevLat = 0
    prevLon = 0
    startLat, startLon = readGPSCoordinate() # starting coordinates
    currentLat = startLat
    currentLon = startLon

    #compare to check if current drone location is past 2.2 m of starting location
    while ((abs(startLat - currentLat) < minStartDistance) and (abs(startLon - currentLon) < minStartDistance)):
        print("Still in starting spot.")
        print("Difference between lat: " + str(abs(currentLat-startLat)))
        print("Difference between lon: " + str(abs(currentLon-startLon)))
        time.sleep(2) 

        currentLat, currentLon = readGPSCoordinate()


    print("Reading Coordinates Now")

    # Capturing webcam footage
    webcam_video = cv2.VideoCapture(0)

    #open csv file to write to
    with open("coordinates.csv","w") as coorfile:
        filewriter = csv.writer(coorfile, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL)
        filewriter.writerow(['Latititude', 'Longtitude'])
        while ((abs(startLat - currentLat) > minStartDistance) or (abs(startLon - currentLon) > minStartDistance)):
            success, video = webcam_video.read() # Reading webcam footage

            img = cv2.cvtColor(video, cv2.COLOR_BGR2HSV) # Converting BGR image to HSV format

            mask = cv2.inRange(img, lower, upper) # Masking the image to find our color

            mask_contours, hierarchy = cv2.findContours(mask, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_SIMPLE) # Finding contours in mask image

            # reads new current coordinates
            currentLat, currentLon = readGPSCoordinate()

            # Finding position of all contours
            if len(mask_contours) != 0:
                for mask_contour in mask_contours:
                    if cv2.contourArea(mask_contour) > 100:
                        x, y, w, h = cv2.boundingRect(mask_contour)
                        cv2.rectangle(video, (x, y), (x + w, y + h), (0, 0, 255), 3) #drawing rectangle
                        
                        # will write to csv file when detected
                        if (round(currentLat, numOfDigits-1) != prevLat and round(currentLon, numOfDigits - 1) != prevLon):
                            # cuts it by one digit when writing to csv file
                            prevLat = round(currentLat, numOfDigits - 1)
                            prevLon = round(currentLon, numOfDigits - 1)
                            filewriter.writerow([prevLat, prevLon])
                            print("Found green spot and recording coor: " + str(prevLat) + ", " + str(prevLon))

            cv2.namedWindow("mask image", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("mask image", 1000, 1000)
            cv2.imshow("mask image", mask) # Displaying mask image
            
            cv2.namedWindow("window", cv2.WINDOW_NORMAL)
            cv2.resizeWindow("window", 1000, 1000)
            cv2.imshow("window", video) # Displaying webcam image

            cv2.waitKey(1)
        print("Back to Starting Location")

if __name__ == "__main__":
    main()

# This code captures video from the default camera and applies color detection to the video frames.
# The code uses OpenCV's cv2 module to perform the image processing operations.

# The lower and upper variables specify the lower and upper range of the yellow color in the HSV color
# space. The video frames are captured using the cv2.VideoCapture class, and the frames are read in a loop.
# In each iteration of the loop, the BGR video frame is converted to the HSV color space using cv2.cvtColor.

# A binary mask is created by thresholding the image using cv2.inRange, and the contours of the yellow color
#  are found using cv2.findContours. If there are any contours found, the code checks the area of each contour,
#  and if the area is greater than 100 pixels, it draws a bounding rectangle around the contour using cv2.rectangle.

# Finally, the mask image and the original video frame with the bounding rectangles are displayed
#  using cv2.imshow. The loop continues until the user presses a key.