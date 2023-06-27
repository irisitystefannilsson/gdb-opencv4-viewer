## Description

originally from:

https://github.com/beenfrog/gdb-opencv-viewer

modified to use opencv4 mats (numpy arrays)


## How to use
* Required packages: opencv, python, numpy
* Clone this repository
```
```
* Add the follow lines in ~/.gdbinit. The alias command is optional.
```
source /FULL-PATH-OF-THE-FILE/cvplot.py
alias view = plot
alias imshow = plot
```
* Usage
```
plot m, the m is an object of cv::Mat1b or cv::Mat3b 
view m, if you set alias view = plot
imshow m, if you set alias imshow = plot
```

## Demo
* debug and view image in gdb:
```
cd gdb-opencv4-viewer
mkdir Debug && cd Debug
cmake -DCMAKE_BUILD_TYPE=Debug .. && make
gdb ./viewer
break 29
run
plot img_color
plot img_gray
```
* view Mat in vector:
if just use the follow command:
```
plot img_vec[0]
plot img_vec[1]
```
we will get:
```
Python Exception <class 'gdb.error'> Could not find operator[].: 
Error occurred in Python command: Could not find operator[].
```
and the right way to view the mat in vector is:
```
pvector img_vec
plot $1
plot $2
```
See more in next section.

* NOTE: There may be some bugs with the imshow in python under GNU/Linux, which make you unable to close the image by click the "close" button on the dialog, but you can just click the image and press any key to close the image dialog.
