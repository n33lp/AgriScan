# iGEM UAlberta Integration Dev

## Installation

### OpenCV

OpenCV was installed for Raspberry Pi using the following [guide] (https://raspberrypi-guide.github.io/programming/install-opencv)

First, make sure to use the following command.
```
sudo apt-get update
```


Next, install the prerequisites:
```
sudo apt-get install build-essential cmake pkg-config libjpeg-dev libtiff5-dev libjasper-dev libpng-dev libavcodec-dev libavformat-dev libswscale-dev libv4l-dev libxvidcore-dev libx264-dev libfontconfig1-dev libcairo2-dev libgdk-pixbuf2.0-dev libpango1.0-dev libgtk2.0-dev libgtk-3-dev libatlas-base-dev gfortran libhdf5-dev libhdf5-serial-dev libhdf5-103 python3-pyqt5 python3-dev -y
```

Finally install openCV using the following command:
```
pip install opencv-python==4.5.3.56
``` 
or
```
sudo apt-get install python-opencv
```

if pip install does not work.
