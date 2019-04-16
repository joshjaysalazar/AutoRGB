# AutoHSV
A Python script to quickly process an image through different HSV values

# How to Use
Edit colors.py to add all the HSV values you want the script to run to. There
are some sample values there to help you get started.

The run the script with three arguments: prefix, file, and destination.
For example:

python autohsv.py new test.png C:\Users\me\Desktop

This will run the image test.png through all the colors in colors.py, then save
each image to the desktop.
