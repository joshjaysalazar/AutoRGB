import tkinter as tk
import tkinter.ttk as ttk
import tkintertable as tktable

class Main(tk.Frame):
    def __init__(self, master=None):
        super().__init__(master)
        self.master = master

        # Give the contents of the window 15px of padding on the sides
        self.grid(row=0, padx=15, pady=15)

        # Original File
        self.original_label = tk.Label(self, text='Original File')
        self.original_label.grid(column=0, row=0, columnspan=4, sticky=tk.W)

        self.original_var = tk.StringVar()
        self.original_var.set('/path/to/file.png')
        self.original_entry = tk.Entry(self, textvariable=self.original_var)
        self.original_entry.grid(column=0, row=1, columnspan=2)

        self.original_button = tk.Button(self, text='Browse...', command=self.browse)
        self.original_button.grid(column=2, row=1, columnspan=2, sticky=tk.E)

        # Destination
        self.destination_label = tk.Label(self, text='Destination')
        self.destination_label.grid(column=0, row=2, columnspan=4, sticky=tk.W)

        self.destination_var = tk.StringVar()
        self.destination_var.set('/path/to/destination')
        self.destination_entry = tk.Entry(self, textvariable=self.destination_var)
        self.destination_entry.grid(column=0, row=3, columnspan=2)

        self.destination_button = tk.Button(self, text='Browse...', command=self.browse)
        self.destination_button.grid(column=2, row=3, columnspan=2, sticky=tk.E)

        # Output Format
        self.output_label = tk.Label(self, text='Output Format (?)')
        self.output_label.grid(column=0, row=4, columnspan=4, sticky=tk.W)

        self.output_var = tk.StringVar()
        self.output_var.set('Image%n_%c')
        self.output_entry = tk.Entry(self, textvariable=self.output_var)
        self.output_entry.grid(column=0, row=5, columnspan=3, sticky=tk.W+tk.E)

        self.output_suffix = tk.Label(self, text='.png')
        self.output_suffix.grid(column=3, row=5, sticky=tk.E)

        # Color Mode
        self.color_mode_label = tk.Label(self, text='Color Mode (?)')
        self.color_mode_label.grid(column=0, row=6, sticky=tk.W)

        self.color_mode_var = tk.StringVar()
        self.color_mode_var.set('shift')
        self.color_mode_shift = tk.Radiobutton(self, text='Shift', variable=self.color_mode_var, value='shift')
        self.color_mode_shift.grid(column=0, row=7, sticky=tk.W)
        self.color_mode_blend = tk.Radiobutton(self, text='Blend', variable=self.color_mode_var, value='blend')
        self.color_mode_blend.grid(column=0, row=8, sticky=tk.W)

        # Process Images
        self.process_images = tk.Button(self, text='Process Images', command=self.process, width = 20, height = 2)
        self.process_images.grid(column=1, row=6, columnspan=3, rowspan=3, sticky=tk.E)

        # Progress Bar
        self.progress_label = tk.Label(self, text='Processing file 0 of 0...')
        self.progress_label.grid(column=0, row=9, columnspan=4, sticky=tk.W)

        self.progress_var = tk.DoubleVar() # Assume that total number of images will be converted to percentage
        self.progress_var.set(0)
        self.progress_bar = ttk.Progressbar(self, variable=self.progress_var, length=200)
        self.progress_bar.grid(column=0, row=10, columnspan=4)

    def browse(self):
        pass

    def process(self):
        pass

def main():
    root = tk.Tk()
    root.title('AutoHSV')

    main = Main(root)

    root.mainloop()
