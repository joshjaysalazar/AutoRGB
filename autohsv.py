#!/usr/bin/python3

# AutoHSV
# by Joshua Jay Salazar
# Released under the GNU General Public License

import sys
import colorsys
from PIL import Image
import os

import colors # Import python file with list of colors

# Parse the arguments given
PREFIX = sys.argv[1]
FILE = sys.argv[2]
DEST = sys.argv[3]

# Open an Image
def open_image(path):
    newImage = Image.open(path)
    return newImage

# Save Image
def save_image(image, path):
    image.save(path, 'png')

# Create a new image with the given size
def create_image(i, j):
    image = Image.new("RGBA", (i, j), "white")
    return image

# Get the pixel from the given image
def get_pixel(image, i, j):
    # Inside image bounds?
    width, height = image.size
    if i > width or j > height:
        return None

    # Get Pixel
    pixel = image.getpixel((i, j))
    return pixel

def convert_image(image, h_adjust, s_adjust, v_adjust):
    # Get size
    width, height = image.size

    # Create new Image and a Pixel Map
    new = create_image(width, height)
    pixels = new.load()

    # Apply HSV filter
    for i in range(width):
        for j in range(height):
            # Get Pixel
            pixel = get_pixel(image, i, j)

            # Get RGBA values (This are int from 0 to 255)
            r = pixel[0]
            g = pixel[1]
            b = pixel[2]
            a = pixel[3]

            # Convert to HSV space
            h ,s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)

            # Convert each value to the value in the list
            h = h_adjust/360
            s = s * s_adjust/100.
            v = v * v_adjust/100.

            # Convert back to RGB
            r, g, b = colorsys.hsv_to_rgb(h, s, v)

            # Set Pixel in new image
            pixels[i, j] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999), a)

    # Return the converted image
    return new


##### Main #####
if __name__ == "__main__":
    # Load Image (JPEG/JPG needs libjpeg to load)
    original = open_image(FILE)

    # Convert image for each value in colors.py
    image_number = 0
    for value in colors.COLORS:
        new = convert_image(original, value[1], value[2], value[3])

        output = os.path.join(DEST, PREFIX + str(image_number) + "_" + value[0] + ".png")
        save_image(new, output)
        image_number += 1
