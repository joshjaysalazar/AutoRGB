#!/usr/bin/python3

# AutoRGB v0.1
# by Joshua Jay Salazar
# Released under the GNU General Public License

import tkinter as tk

import MainWindow
#import recolor

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)
    root.title('AutoRGB')

    main = MainWindow.MainWindow(root)

    root.mainloop()
