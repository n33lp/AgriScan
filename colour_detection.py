import cv2
import numpy as np
import random
import matplotlib.pyplot as plt

def pink_identify():
    try:

        # Initialize the camera
        cam_port = 0  # Adjust this value if you have multiple cameras
        cam = cv2.VideoCapture(cam_port)
        
        # Capture a single frame from the camera
        result, img = cam.read()
        
        if not result:
            return -1
        
        lower_pink =np.array([110, 140, 25], np.uint8)  # good 
        upper_pink =np.array([250, 255, 100], np.uint8) 
        
        pink_mask = cv2.inRange(img, lower_pink, upper_pink)

        kernel = np.ones((5, 5), dtype=np.uint8)
        dilate = cv2.dilate(pink_mask, kernel)

        # Get pink region 
        pink_result = cv2.bitwise_and(img, img, mask = dilate)

        cnts, hierarchy = cv2.findContours(dilate,cv2.RETR_TREE,cv2.CHAIN_APPROX_SIMPLE)

        if len(cnts) == 0:  
            return 0
        else:
            return 1
    except:
        return -1
    
# randomly generates number between -1 and 1 to simulate colour detection
def pink_identify_sim():
    return random.randint(-1,1)