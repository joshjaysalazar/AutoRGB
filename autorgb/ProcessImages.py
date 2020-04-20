import sys
import colorsys
from PIL import Image
from PIL import ImageOps
import os

class ProcessImages():
    def __init__(self, master, original_type, original_path, destination_path, output_format, white_thresh, color_mode, color_list, progress_bar, progress_label, organize):
        # Expose needed variables to all functions in the class
        self.master = master
        self.original_type = original_type
        self.original_path = original_path
        self.destination_path = destination_path
        self.output_format = output_format
        self.white_thresh = white_thresh / 100.
        self.color_mode = color_mode
        self.color_list = color_list
        self.progress_bar = progress_bar
        self.progress_label = progress_label
        self.organize = organize

        print('White Threshold ', self.white_thresh)

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

    def convert_image(self, image, r_adjust, g_adjust, b_adjust):
        # Get size
        width, height = image.size

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
                if len(pixel) > 3: # Check to see if an alpha channel exists
                    a = pixel[3]
                else: # If it doesn't, just set alpha to full
                    a = 255

                # Convert RGB adjust to HSV adjust
                h_adjust, s_adjust, v_adjust = colorsys.rgb_to_hsv(float(r_adjust)/255., float(g_adjust)/255., float(b_adjust)/255.)

                # Convert to HSV space
                h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)

                # Convert each value to the value in the list
                if self.color_mode == 'colorize':
                    # Adjust the pixel if above the white threshold
                    if s <= self.white_thresh and v >= (1. - self.white_thresh):
                        pass
                    else:
                        h = h_adjust
                        s = s * s_adjust
                        v = v * v_adjust
                elif self.color_mode == 'average':
                    if s <= self.white_thresh and v >= (1. - self.white_thresh):
                        pass
                    else:
                        h = (h + h_adjust) / 2
                        s = (s + s_adjust) / 2
                        v = (v + v_adjust) / 2

                # Convert back to RGB
                r, g, b = colorsys.hsv_to_rgb(h, s, v)

                # Set Pixel in new image
                pixels[i, j] = (int(r * 255.9999), int(g * 255.9999), int(b * 255.9999), a)

        # Return the converted image
        return new
