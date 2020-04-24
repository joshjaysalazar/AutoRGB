import tkinter as tk
from tkinter import ttk
import colorsys
from PIL import Image
from PIL import ImageTk

class EditWindow(tk.Frame):
    def __init__(self, master=None, color_list=None, icon_list=None, color_table=None, selected_entry=None, selected_index=None):
        tk.Frame.__init__(self, master)
        self.toplevel = self.winfo_toplevel()

        # Expose the variables from the parents class
        self.colors = color_list
        self.icons = icon_list
        self.color_table = color_table
        self.selected_entry = selected_entry
        self.selected_index = selected_index

        self.current_name = self.color_table.set(self.selected_entry, column='Name')
        self.current_red = self.color_table.set(self.selected_entry, column='R')
        self.current_green = self.color_table.set(self.selected_entry, column='G')
        self.current_blue = self.color_table.set(self.selected_entry, column='B')
        self.current_hue = self.color_table.set(self.selected_entry, column='H')
        self.current_saturation = self.color_table.set(self.selected_entry, column='S')
        self.current_value = self.color_table.set(self.selected_entry, column='V')

        # Rename Color
        self.rename_label = ttk.Label(self, text="Name")
        self.rename_label.grid(column=0, row=0, sticky=tk.E, padx=(0, 10), pady=(0, 10))

        self.rename_var = tk.StringVar()
        self.rename_var.set(self.current_name)
        self.rename_entry = ttk.Entry(self, textvariable=self.rename_var, width=23)
        self.rename_entry.grid(column=1, row=0, columnspan=2, sticky=tk.W, pady=(0, 10))

        # OK and exit when you hit Return in the Name box
        self.rename_entry.bind('<KeyPress-Return>', self.set_and_close)

        # Red Slider
        self.red_label = tk.Label(self, text='R')
        self.red_label.grid(column=0, row=1, stick=tk.E, padx=(0, 10))

        self.red_var = tk.StringVar()
        self.red_var.set(self.current_red)
        self.red_slider = ttk.Scale(self, length=100, orient=tk.HORIZONTAL,
            variable=self.red_var, from_=0, to=255,
            command=lambda s:self.red_var.set('%d' % float(s))) # Sets the output to an integer
        self.red_slider.grid(column=1, row=1, sticky=tk.W, padx=(0, 10))

        # Recalculate colors when the mouse is clicked OR held & moved
        self.red_slider.bind('<Button-1>', lambda x:self.recalculate_color(active='r'))
        self.red_slider.bind('<B1-Motion>', lambda x:self.recalculate_color(active='r'))

        self.red_entry = ttk.Entry(self, textvariable=self.red_var, width=5)
        self.red_entry.grid(column=2, row=1, sticky=tk.W)

        # Recalcuate color when box leaves focus OR when user presses Return
        self.red_entry.bind('<FocusOut>', lambda x:self.recalculate_color(active='r'))
        self.red_entry.bind('<KeyPress-Return>', lambda x:self.recalculate_color(active='r'))

        # Green Slider
        self.green_label = tk.Label(self, text='G')
        self.green_label.grid(column=0, row=2, stick=tk.E, padx=(0, 10))

        self.green_var = tk.StringVar()
        self.green_var.set(self.current_green)
        self.green_slider = ttk.Scale(self, length=100, orient=tk.HORIZONTAL,
            variable=self.green_var, from_=0, to=255,
            command=lambda s:self.green_var.set('%d' % float(s))) # Sets the output to an integer
        self.green_slider.grid(column=1, row=2, sticky=tk.W, padx=(0, 10))

        # Recalculate colors when the mouse is clicked OR held & moved
        self.green_slider.bind('<Button-1>', lambda x:self.recalculate_color(active='g'))
        self.green_slider.bind('<B1-Motion>', lambda x:self.recalculate_color(active='g'))

        self.green_entry = ttk.Entry(self, textvariable=self.green_var, width=5)
        self.green_entry.grid(column=2, row=2, sticky=tk.W)

        # Recalcuate color when box leaves focus OR when user presses Return
        self.green_entry.bind('<FocusOut>', lambda x:self.recalculate_color(active='g'))
        self.green_entry.bind('<KeyPress-Return>', lambda x:self.recalculate_color(active='g'))

        # Blue Slider
        self.blue_label = tk.Label(self, text='B')
        self.blue_label.grid(column=0, row=3, stick=tk.E, padx=(0, 10))

        self.blue_var = tk.StringVar()
        self.blue_var.set(self.current_blue)
        self.blue_slider = ttk.Scale(self, length=100, orient=tk.HORIZONTAL,
            variable=self.blue_var, from_=0, to=255,
            command=lambda s:self.blue_var.set('%d' % float(s))) # Sets the output to an integer
        self.blue_slider.grid(column=1, row=3, sticky=tk.W, padx=(0, 10))

        # Recalculate colors when the mouse is clicked OR held & moved
        self.blue_slider.bind('<Button-1>', lambda x:self.recalculate_color(active='b'))
        self.blue_slider.bind('<B1-Motion>', lambda x:self.recalculate_color(active='b'))

        self.blue_entry = ttk.Entry(self, textvariable=self.blue_var, width=5)
        self.blue_entry.grid(column=2, row=3, sticky=tk.W)

        # Recalcuate color when box leaves focus OR when user presses Return
        self.blue_entry.bind('<FocusOut>', lambda x:self.recalculate_color(active='b'))
        self.blue_entry.bind('<KeyPress-Return>', lambda x:self.recalculate_color(active='b'))

        # Hue Slider
        self.hue_label = tk.Label(self, text='H')
        self.hue_label.grid(column=0, row=4, stick=tk.E, padx=(0, 10))

        self.hue_var = tk.StringVar()
        self.hue_var.set(self.current_hue)
        self.hue_slider = ttk.Scale(self, length=100, orient=tk.HORIZONTAL,
            variable=self.hue_var, from_=0, to=359,
            command=lambda s:self.hue_var.set('%d' % float(s))) # Sets the output to an integer
        self.hue_slider.grid(column=1, row=4, sticky=tk.W, padx=(0, 10))

        # Recalculate colors when the mouse is clicked OR held & moved
        self.hue_slider.bind('<Button-1>', lambda x:self.recalculate_color(active='h'))
        self.hue_slider.bind('<B1-Motion>', lambda x:self.recalculate_color(active='h'))

        self.hue_entry = ttk.Entry(self, textvariable=self.hue_var, width=5)
        self.hue_entry.grid(column=2, row=4, sticky=tk.W)

        # Recalcuate color when box leaves focus OR when user presses Return
        self.hue_entry.bind('<FocusOut>', lambda x:self.recalculate_color(active='h'))
        self.hue_entry.bind('<KeyPress-Return>', lambda x:self.recalculate_color(active='h'))

        # Saturation Slider
        self.saturation_label = tk.Label(self, text='S')
        self.saturation_label.grid(column=0, row=5, stick=tk.E, padx=(0, 10))

        self.saturation_var = tk.StringVar()
        self.saturation_var.set(self.current_saturation)
        self.saturation_slider = ttk.Scale(self, length=100, orient=tk.HORIZONTAL,
            variable=self.saturation_var, from_=0, to=100,
            command=lambda s:self.saturation_var.set('%d' % float(s))) # Sets the output to an integer
        self.saturation_slider.grid(column=1, row=5, sticky=tk.W, padx=(0, 10))

        # Recalculate colors when the mouse is clicked OR held & moved
        self.saturation_slider.bind('<Button-1>', lambda x:self.recalculate_color(active='s'))
        self.saturation_slider.bind('<B1-Motion>', lambda x:self.recalculate_color(active='s'))

        self.saturation_entry = ttk.Entry(self, textvariable=self.saturation_var, width=5)
        self.saturation_entry.grid(column=2, row=5, sticky=tk.W)

        # Recalcuate color when box leaves focus OR when user presses Return
        self.saturation_entry.bind('<FocusOut>', lambda x:self.recalculate_color(active='s'))
        self.saturation_entry.bind('<KeyPress-Return>', lambda x:self.recalculate_color(active='s'))

        # Value Slider
        self.value_label = tk.Label(self, text='V')
        self.value_label.grid(column=0, row=6, stick=tk.E, padx=(0, 10))

        self.value_var = tk.StringVar()
        self.value_var.set(self.current_value)
        self.value_slider = ttk.Scale(self, length=100, orient=tk.HORIZONTAL,
            variable=self.value_var, from_=0, to=100,
            command=lambda s:self.value_var.set('%d' % float(s))) # Sets the output to an integer
        self.value_slider.grid(column=1, row=6, sticky=tk.W, padx=(0, 10))

        # Recalculate colors when the mouse is clicked OR held & moved
        self.value_slider.bind('<Button-1>', lambda x:self.recalculate_color(active='v'))
        self.value_slider.bind('<B1-Motion>', lambda x:self.recalculate_color(active='v'))

        self.value_entry = ttk.Entry(self, textvariable=self.value_var, width=5)
        self.value_entry.grid(column=2, row=6, sticky=tk.W)

        # Recalcuate color when box leaves focus OR when user presses Return
        self.value_entry.bind('<FocusOut>', lambda x:self.recalculate_color(active='v'))
        self.value_entry.bind('<KeyPress-Return>', lambda x:self.recalculate_color(active='v'))

        # Color Preview
        self.color_preview = tk.Canvas(self, width=100, height=100)
        self.color_preview.grid(column=3, row=0, rowspan=5, sticky=tk.NE, padx=(20, 0))

        self.update_color() # Set the initial color

        # OK Button
        self.ok_button = ttk.Button(self, text='OK', command=self.set_and_close)
        self.ok_button.grid(column=3, row=5, rowspan=2, sticky=tk.W+tk.E+tk.N+tk.S, padx=(20, 0))

    def recalculate_color(self, event=None, active=None):
        # Get the changed color number(s)
        r = int(self.red_var.get())
        g = int(self.green_var.get())
        b = int(self.blue_var.get())
        h = int(self.hue_var.get())
        s = int(self.saturation_var.get())
        v = int(self.value_var.get())

        # If RGB changed, recalculate HSV
        if active == 'r' or active == 'g' or active == 'b':
            h, s, v = colorsys.rgb_to_hsv(r/255., g/255., b/255.)
            h = int(h * 359.)
            s = int(s * 100.)
            v = int(v * 100.)

            # Set the HSV sliders
            self.hue_var.set(h)
            self.saturation_var.set(s)
            self.value_var.set(v)

        # If HSV changed, recalculate RGB
        if active == 'h' or active == 's' or active == 'v':
            r, g, b = colorsys.hsv_to_rgb(h/359., s/100., v/100.)
            r = int(r * 255.)
            g = int(g * 255.)
            b = int(b * 255.)

            # Set the RGB sliders
            self.red_var.set(r)
            self.green_var.set(g)
            self.blue_var.set(b)

        # Update the color preview
        self.update_color()

    def update_color(self):
        # Calculate hex RGB color code
        hex_red = hex(int(self.red_var.get()))[2:] # returns something like '0x15', so we remove the '0x'
        hex_red = '0' + hex_red if len(hex_red) < 2 else hex_red # make sure 2 digits
        hex_green = hex(int(self.green_var.get()))[2:]
        hex_green = '0' + hex_green if len(hex_green) < 2 else hex_green
        hex_blue = hex(int(self.blue_var.get()))[2:]
        hex_blue = '0' + hex_blue if len(hex_blue) < 2 else hex_blue
        self.color_code = '#' + hex_red + hex_green + hex_blue

        # Update the preview
        self.color_preview.config(bg=self.color_code)

    def set_and_close(self, event=None):
        # Create color swatch
        swatch = Image.new(mode='RGB', size=(16, 16), color=(int(self.red_var.get()), int(self.green_var.get()), int(self.blue_var.get())))
        self.icons[self.selected_index] = ImageTk.PhotoImage(swatch)

        # Update the table entry
        self.color_table.item(self.selected_entry, image=self.icons[self.selected_index])
        self.color_table.set(self.selected_entry, column='Name', value=self.rename_var.get())
        self.color_table.set(self.selected_entry, column='R', value=self.red_var.get())
        self.color_table.set(self.selected_entry, column='G', value=self.green_var.get())
        self.color_table.set(self.selected_entry, column='B', value=self.blue_var.get())
        self.color_table.set(self.selected_entry, column='H', value=self.hue_var.get())
        self.color_table.set(self.selected_entry, column='S', value=self.saturation_var.get())
        self.color_table.set(self.selected_entry, column='V', value=self.value_var.get())

        # Update the colors array
        self.colors[self.selected_index][0] = self.rename_var.get()
        self.colors[self.selected_index][1] = self.red_var.get()
        self.colors[self.selected_index][2] = self.green_var.get()
        self.colors[self.selected_index][3] = self.blue_var.get()

        # Destroy the window
        self.toplevel.destroy()
