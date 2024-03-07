import numpy as np
from glob import glob
import cv2
import matplotlib.pyplot as plt
from PIL import Image
import sklearn
from sklearn.cluster import KMeans
from collections import Counter
from skimage.color import rgb2lab, deltaE_cie76
import os
from PIL import Image

def pink_identify():
    '''
    returns:
        -1: webacam error fly back to starting position
        0: no fungal presense
        1: fungal presensem, save the lat lon
    '''
    
    '''
    ret: This is a boolean value (True or False) that indicates whether a frame was successfully read.
        If ret is True, it means a frame was successfully captured from the source (webcam in this case).
        If ret is False, it indicates that there was an issue capturing a frame.

    frame: This is the actual image data of the captured frame. It's a NumPy array representing the image.
        You can perform various image processing operations on this array.
    
    cap: is the video capture object obtained by cv2.VideoCapture(0) (which opens the default webcam),

    '''

    cap = cv2.VideoCapture(0)  # Open the webcam

    ret, frame = cap.read()  # Read a frame from the webcam

    cap.release()  # Release the webcam

    if not ret:
        print("Failed to capture image from webcam.")
        return -1

    blurred_image = cv2.GaussianBlur(frame, (5, 5), 0)
    hsv = cv2.cvtColor(blurred_image, cv2.COLOR_BGR2HSV)

    lower_pink = np.array([330/2, 50, 50])
    upper_pink = np.array([350/2, 255, 255])
    

    # mask = cv2.inRange(hsv, lower_pink, upper_pink)
    pink_mask = cv2.inRange(hsv, lower_pink,     upper_pink)


    kernel = np.ones([5, 5], dtype=np.uint8)
    dilate = cv2.dilate(pink_mask, kernel, iterations=1)

    # contour
    cnts, hierarchy = cv2.findContours(dilate, cv2.RETR_EXTERNAL, cv2.CHAIN_APPROX_NONE)

    print("try get contour")
    if len(cnts) == 0:
        print("no counter find")
        cv2.imshow("pink_identify", frame)
        return
    
    # get pink region 
    pink_result = cv2.bitwise_and(image, image, pink_mask)

    max_cnt = max(cnts, key=cv2.contourArea)
    cv2.drawContours(frame, max_cnt, -1, (0, 0, 255), 2)

    (x, y, w, h) = cv2.boundingRect(max_cnt)
    cv2.rectangle(frame, (x, y), (x + w, y + h), (0, 0, 255), 3)

    # cv2.imshow("pink_identify", img)
    cv2.imshow('Pink Detection', pink_result)

    plt.imshow(frame)
    plt.show()


if __name__ == "__main__":
    cell_files = glob("/Users/rayna/Documents/IGEM/AI-Model/Image_RGB/*.JPG")
    image_path = cell_files[3]
    image = plt.imread(image_path) # BGR
    plt.imshow(image) # RGB
    plt.show()

    # cv2.imshow("image",image)
    pink_identify(image)