import sys
import colorsys
from PIL import Image
from PIL import ImageOps
import os
import math

class ProcessImages():
    def __init__(self, master, original_type, original_path, destination_path, output_format, midpoint, color_mode, color_list, progress_bar, progress_label, organize):
        # Expose needed variables to all functions in the class
        self.master = master
        self.original_type = original_type
        self.original_path = original_path
        self.destination_path = destination_path
        self.output_format = output_format
        self.midpoint = midpoint
        self.color_mode = color_mode
        self.color_list = color_list
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.organize = organize

        self.progress_bar.set(0.0)
        self.number_of_images = 0
        self.total_processed = 0

        if self.original_type == 'file':
            self.number_of_images = 1 # set number of images to 1
            self.process_file(self.original_path, self.destination_path)
        elif self.original_type == 'folder':
            self.number_of_images = 0 # reset the image count
            # Count the number of PNGs in the folder
            for file in os.listdir(self.original_path):
                if file.endswith('.png'):
                    self.number_of_images += 1

            # Convert each file with a .png ending
            for file in os.listdir(self.original_path):
                if file.endswith('.png'):
                    # Set path to current working file
                    path = os.path.join(self.original_path, file)

                    if self.organize == 'file':
                        # Create a directory to send new files to
                        folder_name = file[:-4] # Strip the .png off the end of the file name
                        destination = self.destination_path + '/' + folder_name
                        # If the folder doesn't exist yet, create it
                        if not os.path.exists(destination):
                            os.mkdir(destination)
                    else:
                        destination = self.destination_path

                    # Process those files!
                    self.process_file(path, destination)

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
            output_name = output_name.replace('%r', str(value[1])) # Replace %r with the red value
            output_name = output_name.replace('%g', str(value[2])) # Replace %g with the green value
            output_name = output_name.replace('%b', str(value[3])) # Replace %b with the blue value
            output_name = output_name.replace('%h', str(value[4])) # Replace %h with the hue value
            output_name = output_name.replace('%s', str(value[5])) # Replace %s with the saturation value
            output_name = output_name.replace('%v', str(value[6])) # Replace %v with the value value
            output_name = output_name.replace('%o', os.path.basename(file)[:-4]) # Repalce %o with original file name - .png
            output_name = output_name + '.png' # Add the .png suffix

            if self.organize == 'color':
                # Output the file and organize according to color
                sorted = destination + '/' + value[0]
                if not os.path.exists(sorted):
                    os.mkdir(sorted)
                new_output = os.path.join(sorted, output_name)
            else:
                new_output = os.path.join(destination, output_name)
            self.save_image(new, new_output)

            # Update progress
            self.total_processed += 1
            self.update_progress()

            # Increment image number
            image_number += 1

    def update_progress(self):
        total_queued = len(self.color_list) * self.number_of_images
        if self.total_processed < total_queued:
            progress_out_of = 'Processed image ' + str(self.total_processed) + ' of ' + str(total_queued) + '...'
            self.progress_label.config(text=progress_out_of)
        elif self.total_processed == total_queued:
            self.progress_label.config(text='Finished processing ' + str(total_queued) + ' images.')
        elif self.total_processed == 0:
            self.progress_label.config(text='Ready.')
        else:
            self.progress_label.config(text='Error.')

        progress_percentage = (self.total_processed / total_queued) * 100 # Get the progress in percent
        self.progress_bar.set(progress_percentage) # Update the progress bar

        # Make sure to update the tkinter window, or the program appears frozen
        self.master.update()

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

    def convert_image(self, original, r_adjust, g_adjust, b_adjust):
        """
        Convert an image by adjusting its color properties.

        Args:
            original (PIL.Image.Image): The original image to convert.
            r_adjust (float): The red channel adjustment factor.
            g_adjust (float): The green channel adjustment factor.
            b_adjust (float): The blue channel adjustment factor.

        Returns:
            PIL.Image.Image: The converted image.

        Raises:
            None

        Example:
            >>> original = Image.open("path/to/image.png")
            >>> r_adjust = 1.2
            >>> g_adjust = 0.8
            >>> b_adjust = 1.0
            >>> converted_image = convert_image(
                    original, r_adjust, g_adjust, b_adjust
                )

        Notes:
            - The function uses two different methods for image conversion:
              1. Colorization: Adjust the grayscale contrast and colorize image.
              2. Shift: Adjusts the color channels with a given midpoint.
            - The function also handles alpha channels.
        """
        # Separate the alpha channel
        alpha = original.getchannel('A')

        # Convert to grayscale & adjust contrast so black and white are both present
        gray = ImageOps.grayscale(original)

        if self.color_mode == 'colorize':
            # If the top-left pixel is fully transparent, ignore the transparent background on the autocontrast function
            transparent = original.getpixel((0, 0))[3]
            if transparent == 0:
                do_ignore = 0
            else:
                do_ignore = None

            # Adjust contrast so true black and true white exist
            contrast = ImageOps.autocontrast(gray, ignore=do_ignore)

            # Colorize the grayscale image
            result = ImageOps.colorize(contrast, (int(r_adjust), int(g_adjust), int(b_adjust)), 'white')

        if self.color_mode == 'shift':
            # Colorize the grayscale image w/ a midpoint setting
            result = ImageOps.colorize(gray, 'black', 'white', (int(r_adjust), int(g_adjust), int(b_adjust)),
                midpoint=self.midpoint)

        # Add the alpha channel back in
        result.putalpha(alpha)

        # Return the converted image
        return result
