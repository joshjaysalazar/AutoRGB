import tkinter as tk
from tkinter import ttk
from tkinter import filedialog
from tkinter import colorchooser
import json

class MainWindow(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Create color table
        self.colors = {}

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
        self.output_label = tk.Label(self, text='Output Format (?)')
        self.output_label.grid(column=0, row=4, columnspan=4, sticky=tk.W)

        self.output_var = tk.StringVar()
        self.output_var.set('Image%n_%c')
        self.output_entry = ttk.Entry(self, textvariable=self.output_var)
        self.output_entry.grid(column=0, row=5, columnspan=3, sticky=tk.W+tk.E)

        self.output_suffix = tk.Label(self, text='.png')
        self.output_suffix.grid(column=3, row=5, sticky=tk.E)

        # Color Mode
        self.color_mode_label = tk.Label(self, text='Color Mode (?)')
        self.color_mode_label.grid(column=0, row=6, sticky=tk.W)

        self.color_mode_var = tk.StringVar()
        self.color_mode_var.set('shift')
        self.color_mode_shift = ttk.Radiobutton(self, text='Shift', variable=self.color_mode_var, value='shift')
        self.color_mode_shift.grid(column=0, row=7, sticky=tk.W)
        self.color_mode_blend = ttk.Radiobutton(self, text='Blend', variable=self.color_mode_var, value='blend')
        self.color_mode_blend.grid(column=0, row=8, sticky=tk.W)

        # Process Images
        self.process_images = ttk.Button(self, text='Process Images', command=self.process, width = 20)
        self.process_images.grid(column=1, row=6, columnspan=3, rowspan=3, sticky=tk.E)

        # Progress Bar
        self.progress_label = tk.Label(self, text='Processing file 0 of 0...')
        self.progress_label.grid(column=0, row=9, columnspan=4, sticky=tk.W)

        self.progress_var = tk.DoubleVar() # Assume that total number of images will be converted to percentage
        self.progress_var.set(0)
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, length=200)
        self.progress_bar.grid(column=0, row=10, columnspan=4)

        # Color Table (Starts at column 4)
        self.color_table = ttk.Treeview(self, columns=('Name', 'H', 'S', 'V'), displaycolumns='#all')
        self.color_table.grid(column=4, row=0, rowspan=9, columnspan=3, padx=10)

        self.color_table.heading('Name', text='Name', anchor=tk.W)
        self.color_table.heading('H', text='H')
        self.color_table.heading('S', text='S')
        self.color_table.heading('V', text='V')

        self.color_table.column('#0', width=30)
        self.color_table.column('Name', width=200)
        self.color_table.column('H', width=40)
        self.color_table.column('S', width=40)
        self.color_table.column('V', width=40)

        # Preset Buttons & Add Color Button
        self.load_preset = ttk.Button(self, text='Load Preset', command=self.load_preset)
        self.load_preset.grid(column=4, row=10)

        self.save_preset = ttk.Button(self, text='Save Preset', command=self.browse)
        self.save_preset.grid(column=5, row=10)

        self.add_color = ttk.Button(self, text='Add Color', command=self.add_color)
        self.add_color.grid(column=6, row=10)

    def load_preset(self):
        self.color_table.insert(parent='', index='end', values=('Test', 250, 100, 100))
        self.color_table.insert(parent='', index='end', values=('Test2', 1, 2, 3))
        self.color_table.insert(parent='', index='end', values=('Test3', 50, 50, 50))

    def browse_original(self):
        if self.original_type_var.get() == 'file':
            target = filedialog.askopenfilename(title='Select File', defaultextension='.png', filetypes=(('Portable Network Graphics (.png)','*.png'), ('All Files','*.*')))
            self.original_var.set(target)
        elif self.original_type_var.get() == 'folder':
            target = filedialog.askdirectory(title='Select Folder')
            self.original_var.set(target)
        print(self.original_var.get())

    def browse_destination(self):
        target = filedialog.askdirectory(title='Select Folder')
        self.destination_var.set(target)

    def browse(self):
        pass

    def process(self):
        pass

    def add_color(self):
        new_color = colorchooser.askcolor()
        if new_color != (None, None):
            print ("whoops")
