import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
import json
import colorsys

import RenameWindow
import ProcessImages
import CreateToolTip

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Create empty color table
        self.colors = []

        # Give the contents of the window 15px of padding on the sides
        self.grid(row=0, padx=15, pady=15)

        # Original File/Folder
        self.original_label = tk.Label(self, text='Original')
        self.original_label.grid(column=0, row=0, columnspan=4, sticky=tk.W)

        self.original_type_var = tk.StringVar()
        self.original_type_var.set('file')
        self.original_type_file = ttk.Radiobutton(self, text='File', variable=self.original_type_var, value='file')
        self.original_type_file.grid(column=1, row=0, sticky=tk.W)
        self.original_type_folder = ttk.Radiobutton(self, text='Folder', variable=self.original_type_var, value='folder')
        self.original_type_folder.grid(column=2, row=0, sticky=tk.W)

        self.original_var = tk.StringVar()
        self.original_var.set('/path/to/file.png')
        self.original_entry = ttk.Entry(self, textvariable=self.original_var)
        self.original_entry.grid(column=0, row=1, columnspan=2)

        self.original_button = ttk.Button(self, text='Browse...', command=self.browse_original)
        self.original_button.grid(column=2, row=1, columnspan=2, sticky=tk.E)

        # Destination
        self.destination_label = tk.Label(self, text='Destination')
        self.destination_label.grid(column=0, row=2, columnspan=4, sticky=tk.W)

        self.destination_var = tk.StringVar()
        self.destination_var.set('/path/to/destination')
        self.destination_entry = ttk.Entry(self, textvariable=self.destination_var)
        self.destination_entry.grid(column=0, row=3, columnspan=2)

        self.destination_button = ttk.Button(self, text='Browse...', command=self.browse_destination)
        self.destination_button.grid(column=2, row=3, columnspan=2, sticky=tk.E)

        # Output Format
        self.output_label = tk.Label(self, text='Output Format')
        self.output_label.grid(column=0, row=4, columnspan=4, sticky=tk.W)

        self.output_var = tk.StringVar()
        self.output_var.set('%o_%c')
        self.output_entry = ttk.Entry(self, textvariable=self.output_var)
        self.output_entry.grid(column=0, row=5, columnspan=3, sticky=tk.W+tk.E)

        self.output_tooltip = CreateToolTip.CreateToolTip(self.output_entry, \
                                                          '%n = Image Number\n'
                                                          '%c = Name of Color\n'
                                                          '%r = Red Value\n'
                                                          '%g = Green Value\n'
                                                          '%b = Blue Value\n'
                                                          '%o = Original File Name')

        self.output_suffix = tk.Label(self, text='.png')
        self.output_suffix.grid(column=3, row=5, sticky=tk.E)

        # Organize By
        self.organize_label = tk.Label(self, text='Organize by:')
        self.organize_label.grid(column=0, row=6, sticky=tk.W, pady=5)

        self.organize_by_var = tk.StringVar()
        self.organize_by_var.set('file')
        self.organize_by_file = ttk.Radiobutton(self, text='File', variable=self.organize_by_var, value='file')
        self.organize_by_file.grid(column=1, row=6, sticky=tk.W)
        self.organize_by_color = ttk.Radiobutton(self, text='Color', variable=self.organize_by_var, value='color')
        self.organize_by_color.grid(column=2, row=6, sticky=tk.W)

        # Color Mode
        self.color_mode_label = tk.Label(self, text='Color Mode')
        self.color_mode_label.grid(column=0, row=7, sticky=tk.W)

        self.color_mode_var = tk.StringVar()
        self.color_mode_var.set('colorize')
        self.color_mode_colorize = ttk.Radiobutton(self, text='Colorize', variable=self.color_mode_var, value='colorize')
        self.color_mode_colorize.grid(column=0, row=8, sticky=tk.W)
        self.colorize_tooltip = CreateToolTip.CreateToolTip(self.color_mode_colorize, 'Converts every color in the image to a relative shade of the new color')
        self.color_mode_average = ttk.Radiobutton(self, text='Average', variable=self.color_mode_var, value='average')
        self.color_mode_average.grid(column=0, row=9, sticky=tk.W)
        self.average_tooltip = CreateToolTip.CreateToolTip(self.color_mode_average, 'Blends to the average of the original color and the new color')

        # Process Images
        self.process_images = ttk.Button(self, text='Process Images', command=self.process_image_files, width = 20)
        self.process_images.grid(column=1, row=7, columnspan=3, rowspan=3, sticky=tk.E+tk.N+tk.S, padx=(10, 0), pady=(10,0))

        # Progress Bar
        self.progress_label = tk.Label(self, text='Ready.')
        self.progress_label.grid(column=0, row=10, columnspan=4, sticky=tk.W)

        self.progress_var = tk.DoubleVar() # Assume that total number of images will be converted to percentage
        self.progress_var.set(0)
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var)
        self.progress_bar.grid(column=0, row=11, columnspan=4, sticky=tk.E+tk.W)

        # Color Table (Starts at column 4)
        self.color_table = ttk.Treeview(self, columns=('Name', 'R', 'G', 'B', 'H', 'S', 'V'), displaycolumns='#all', show='headings')
        self.color_table.grid(column=4, row=0, rowspan=10, columnspan=6, padx=10)
        self.color_table.bind('<Double-1>', self.edit_color)

        self.color_table.heading('Name', text='Name', anchor=tk.W)
        self.color_table.heading('R', text='R')
        self.color_table.heading('G', text='G')
        self.color_table.heading('B', text='B')
        self.color_table.heading('H', text='H')
        self.color_table.heading('S', text='S')
        self.color_table.heading('V', text='V')

        self.color_table.column('#0', width=50)
        self.color_table.column('Name', width=200)
        self.color_table.column('R', width=50)
        self.color_table.column('G', width=50)
        self.color_table.column('B', width=50)
        self.color_table.column('H', width=50)
        self.color_table.column('S', width=50)
        self.color_table.column('V', width=50)

        # Preset Buttons
        self.load_preset_button = ttk.Button(self, text='Load Preset', command=self.load_preset_file)
        self.load_preset_button.grid(column=4, row=11, padx=(10,0))

        self.save_preset_button = ttk.Button(self, text='Save Preset', command=self.save_preset_file)
        self.save_preset_button.grid(column=5, row=11)

        self.add_color_button = ttk.Button(self, text='Add Color', command=self.add_color)
        self.add_color_button.grid(column=6, row=11)

        self.edit_color_button = ttk.Button(self, text='Edit Color', command=self.edit_color)
        self.edit_color_button.grid(column=7, row=11)

        self.remove_color_button = ttk.Button(self, text='Remove Color', command=self.remove_color)
        self.remove_color_button.grid(column=8, row=11)

        self.rename_color_button = ttk.Button(self, text='Rename Color', command=self.rename_color)
        self.rename_color_button.grid(column=9, row=11, padx=(0, 10))

    def browse_original(self):
        if self.original_type_var.get() == 'file':
            target = filedialog.askopenfilename(title='Select File', defaultextension='.png', filetypes=(('Portable Network Graphics (.png)','*.png'), ('All Files','*.*')))
            self.original_var.set(target)
        elif self.original_type_var.get() == 'folder':
            target = filedialog.askdirectory(title='Select Folder')
            self.original_var.set(target)

    def browse_destination(self):
        target = filedialog.askdirectory(title='Select Folder')
        self.destination_var.set(target)

    def load_preset_file(self):
        # Load a json file with colors listed
        target = filedialog.askopenfilename(title='Select File', defaultextension='.json', filetypes=(('JavaScript Object Notation (.json)','*.json'), ('All Files','*.*')))
        if target != '': # Make sure the user didn't cancel
            with open(target, "r") as read_file:
                data = json.load(read_file)

        # Clear self.colors to prepare for a new color list
        self.colors = []

        # Loop through every color in the file & convert each to a list item in self.colors
        for color in data:
            new_value = []
            for i in range(7): # Number of values per color in a preset
                new_value.append(color[i])
            self.colors.append(new_value)

        # Clear the color table
        for color in self.color_table.get_children():
            self.color_table.delete(color)

        # Add each color to the color table
        for color in self.colors:
            self.color_table.insert(parent='', index='end', values=color)

    def save_preset_file(self):
        # Create a new JSON file to save self.colors
        target = filedialog.asksaveasfilename(title='Save As...', defaultextension='.json', filetypes=(('JavaScript Object Notation (.json)','*.json'), ('All Files','*.*')))
        if target != '': # Make sure the user didn't cancel
            with open(target, "w") as write_file:
                json.dump(self.colors, write_file, indent=2)

    def process_image_files(self):
        # Gather all the data needed to run
        master = self.master
        original_type = self.original_type_var.get()
        original_path = self.original_var.get()
        destination_path = self.destination_var.get()
        output_format = self.output_var.get()
        color_mode = self.color_mode_var.get()
        color_list = self.colors
        progress_bar = self.progress_var
        progress_label = self.progress_label
        organize = self.organize_by_var.get()

        # Convert!
        new_images = ProcessImages.ProcessImages(master, original_type, original_path, destination_path, output_format, color_mode, color_list, progress_bar, progress_label, organize)
        del new_images

    def add_color(self):
        # Bring up color chooser window
        new_color = colorchooser.askcolor()

        # If the user didn't click cancel, add the color to self.colors and to self.color_table
        if new_color != (None, None):
            # Extract the default name and color values into their own variables
            name, r, g, b = new_color[1], int(new_color[0][0]), int(new_color[0][1]), int(new_color[0][2])

            # Get HSV values based on RGB values
            h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
            h = int(h * 255.9999)
            s = int(s * 255.9999)
            v = int(v * 255.9999)

            # Create the new list item and add it to self.colors and self.color_table
            new_value = [name, r, g, b, h, s, v]
            self.colors.append(new_value)
            self.color_table.insert(parent='', index='end', values=new_value)

    def edit_color(self, event=None):
        if self.color_table.selection() != (): # Make sure the user hasn't selected nothing, otherwise an error will be thrown
            selected_entry = self.color_table.selection()[0] # Get the selection the user has chosen
            selected_index = self.color_table.index(selected_entry) # Get that selection's index number

            # Bring up color chooser window
            new_color = colorchooser.askcolor()

            # If the user didn't click cancel, edit the color in self.colors and in self.color_table
            if new_color != (None, None):
                # Extract the default name and color values into their own variables
                name, r, g, b = new_color[1], int(new_color[0][0]), int(new_color[0][1]), int(new_color[0][2])

                # Get HSV values based on RGB values, set them to 0-255 scale
                h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
                h = int(h * 255.9999)
                s = int(s * 255.9999)
                v = int(v * 255.9999)

                # Create the revised list item and edit self.colors and self.color_table
                new_value = [name, r, g, b, h, s, v]
                self.colors[selected_index] = new_value
                self.color_table.item(selected_entry, values=new_value)

    def remove_color(self):
        if self.color_table.selection() != (): # Make sure the user hasn't selected nothing, otherwise an error will be thrown
            selected_entry = self.color_table.selection()[0] # Get the selection the user has chosen
            selected_index = self.color_table.index(selected_entry) # Get that selection's index number

            # Delete the value from the color table and color list
            self.color_table.delete(selected_entry)
            del self.colors[selected_index]

    def rename_color(self, event=None):
        if self.color_table.selection() != (): # Make sure the user hasn't selected nothing, otherwise an error will be thrown
            selected_entry = self.color_table.selection()[0] # Get the selection the user has chosen
            selected_index = self.color_table.index(selected_entry) # Get that selection's index number

            # Bring up a dialog to rename (the RenameWindow class does the heavy lifting here)
            window = tk.Toplevel(self)
            window.wm_title('Rename Color')
            window.attributes("-toolwindow", 1)

            frame = RenameWindow.RenameWindow(window, self.colors, self.color_table, selected_entry, selected_index)
            frame.grid(padx=10, pady=10)

            # Position the window reasonably within the main window
            window.update_idletasks() # Make sure size & position are up to date
            win_width, win_height = window.winfo_width(), window.winfo_height()
            main_x, main_y = self.master.winfo_x(), self.master.winfo_y()
            window.geometry('%dx%d+%d+%d' % (win_width, win_height, main_x + 300, main_y + 100))

            # Focus the popup
            window.focus_force()
