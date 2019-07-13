import sys
import colorsys
from PIL import Image
import os

class ProcessImages():
    def __init__(self, original_type, original_path, destination_path, output_format, color_mode, color_list):
        # Expose needed variables to all functions in the class
        self.original_type = original_type
        self.original_path = original_path
        self.destination_path = destination_path
        self.output_format = output_format
        self.color_mode = color_mode
        self.color_list = color_list

        if self.original_type == 'file':
            self.process_file(self.original_path, self.destination_path)
        elif self.original_type == 'folder':
            pass

    def process_file(self, file, destination):
        # Load Image (JPEG/JPG needs libjpeg to load)
        original = self.open_image(file)

        # Convert image for each value in colors.py
        image_number = 1

        # Run the conversion for each color and save the output file
        for value in self.color_list:
            new = self.convert_image(original, value[1], value[2], value[3])

            # Create a string for the current image number
            image_number_string = str(image_number)
            if image_number < 10:
                image_number_string = "0" + image_number_string

            # Set up the output filename based on the user's formatting
            output_name = self.output_format
            output_name = output_name.replace('%n', image_number_string) # Replace %n with the image number
            output_name = output_name.replace('%c', value[0]) # Replace %c with the color name
            output_name = output_name + '.png' # Add the .png suffix

            # Output the file
            output = os.path.join(destination, output_name)
            self.save_image(new, output)
            image_number += 1

    # Open an Image
    def open_image(self, path):
        newImage = Image.open(path)
        return newImage

    # Save Image
    def save_image(self, image, path):
        image.save(path, 'png')

    # Create a new image with the given size
    def create_image(self, i, j):
        image = Image.new("RGBA", (i, j), "white")
        return image

    # Get the pixel from the given image
    def get_pixel(self, image, i, j):
        # Inside image bounds?
        width, height = image.size
        if i > width or j > height:
            return None

        # Get Pixel
        pixel = image.getpixel((i, j))
        return pixel

    def convert_image(self, image, r_adjust, g_adjust, b_adjust):
        # Get size
        width, height = image.size

        # Convert RGB adjust to HSV adjust
        h_adjust, s_adjust, v_adjust = colorsys.rgb_to_hsv(r_adjust/255., g_adjust/255., b_adjust/255.)

        # Create new Image and a Pixel Map
        new = self.create_image(width, height)
        pixels = new.load()

        # Apply HSV filter
        for i in range(width):
            for j in range(height):
                # Get Pixel
                pixel = self.get_pixel(image, i, j)

                # Get RGBA values (This are int from 0 to 255)
                r = pixel[0]
                g = pixel[1]
                b = pixel[2]
                a = pixel[3]

                # Convert to HSV space
                h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)

                # Convert each value to the value in the list
                h = h_adjust
                s = s * s_adjust
                v = v * v_adjust

                # Convert back to RGB
                r, g, b = colorsys.hsv_to_rgb(h, s, v)

                # Set Pixel in new image
                pixels[i, j] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999), a)

        # Return the converted image
        return new
