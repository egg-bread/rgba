# =====================
# import libraries
# =====================
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from PIL import Image, ImageTk

# =====================
# where the magic happens
# =====================
def about():
    pass

def open_file():
    pass

def help():
    pass

# set up gui layout & other settings
root = tk.Tk()
root.option_add("*tearOff", False)
root.title("Colors!!")

mainframe = ttk.Frame(root, padding="5")
mainframe.grid(column=0, row=0)
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# create menu and menu items
win = tk.Toplevel(root)
menubar = tk.Menu(win)
win["menu"] = menubar # configure 'menu' option to attach menu widget to window

menu_file = tk.Menu(menubar) # File menu
menu_other = tk.Menu(menubar) # Other menu

menubar.add_cascade(menu=menu_file, label="File")
menu_file.add_command(label="Open...", command=open_file)

menubar.add_cascade(menu=menu_other, label="Other")
menu_other.add_command(label="Help", command=help)
menu_other.add_command(label="About", command=about)


# ttk.Label(mainframe, text="Hello!").grid(column=0, row=0)

# pil_image = Image.open(filedialog.askopenfile())
# palette_list = Image.getpalette(pil_image)

# for use anywhere on gui by tkinter
# img = ImageTk.PhotoImage(pil_image)

root.mainloop()
