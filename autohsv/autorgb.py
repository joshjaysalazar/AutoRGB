import tkinter as tk

import MainWindow
#import recolor

if __name__ == '__main__':
    root = tk.Tk()
    root.resizable(0, 0)
    root.title('AutoRGB')

    main = MainWindow.MainWindow(root)

    root.mainloop()
