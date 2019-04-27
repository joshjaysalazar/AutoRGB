import tkinter as tk

import MainWindow
#import recolor

if __name__ == '__main__':
    root = tk.Tk()
    root.title('AutoHSV')

    main = MainWindow.MainWindow(root)

    root.mainloop()
