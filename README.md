# Give-Me-A-Chrismas-Hat
add a Chrismas hat :)

Original photo:

![](https://github.com/YeGuanDS/Give-Me-A-Chrismas-Hat/blob/master/person.jpg)

I get a hat now:

![](https://github.com/YeGuanDS/Give-Me-A-Chrismas-Hat/blob/master/output.jpg)

## Requirements
1. [Python==3](https://www.anaconda.com/download/#linux)
2. [OpenCV==3.3](https://docs.opencv.org/3.0-beta/doc/py_tutorials/py_setup/py_table_of_contents_setup/py_table_of_contents_setup.html#py-table-of-content-setup)
3. Boost Python==1.65.1 (conda install boost)
4. [Dlib==19.8.99](https://github.com/davisking/dlib)
5. [Pretrained face landmark detector](http://dlib.net/files/shape_predictor_5_face_landmarks.dat.bz2)

## How to run
1. Make sure you have hat image, photo, and face landmark detector in the same folder
2. Then run: python addHat.py hat.png person.jpg


## Acknowledgement
This repo is adapted from [Liu's work](https://github.com/LiuXiaolong19920720/Add-Christmas-Hat)
