import tkinter as tk
from tkinter import ttk

class RenameWindow(tk.Frame):
    def __init__(self, master=None, color_list=None, color_table=None, selected_entry=None, selected_index=None):
        tk.Frame.__init__(self, master)
        self.toplevel = self.winfo_toplevel()

        # Expose the variables from the parents class
        self.colors = color_list
        self.color_table = color_table
        self.selected_entry = selected_entry
        self.selected_index = selected_index

        self.rename_var = tk.StringVar()
        self.rename_var.set('')
        self.rename_entry = ttk.Entry(self, textvariable=self.rename_var)
        self.rename_entry.grid(column=0, row=0)

        self.button = ttk.Button(self, text="Rename", command=self.rename_and_close)
        self.button.grid(column=1, row=0, padx=(10, 0))

    def rename_and_close(self):
        print(self.selected_entry)
        self.color_table.set(self.selected_entry, column='Name', value=self.rename_var.get()) # Update the table
        self.colors[self.selected_index][0] = self.rename_var.get() # Update the colors array
        self.toplevel.destroy()
