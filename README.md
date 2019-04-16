# AutoHSV
A Python script to quickly process an image through different HSV values

# Required Libaries
This script runs on Python 3, and requires the additional library Pillow. It can
be installed by running the following command:

pip install pillow

# How to Use
Edit colors.py to add all the HSV values you want the script to run to. There
are some sample values there to help you get started.

Then run the script with three arguments: prefix, file, and destination.
For example:

python autohsv.py new smiley.png C:\Users\me\Desktop

(The image you're using must be in the same directory as the script)

This will run the image test.png through all the colors in colors.py, then save
each image to the desktop as "new_color.png" where color is replaced with the
name of the color in colors.py.
