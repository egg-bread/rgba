# =====================
# import libraries
# =====================
import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from PIL import Image, ImageTk

# =====================
# where the magic happens
# =====================
computer_file = ""

def about():
    messagebox.showinfo(title="About", message='''A little program about colors in images :-)
Made in Python using Tkinter''')

# CONVERT TO BUTTON
def open_file():
    global computer_file
    pil_image = Image.open(filedialog.askopenfilename(title="Select an image!")) # opens as a PIL image
    computer_file = ImageTk.PhotoImage(pil_image) # PIL image is made Tkinter-compatible

# CONVERT TO BUTTON
def open_url():
    global computer_file
    # pil_image = Image.open("url")
    # computer_file = ImageTk.PhotoImage(pil_image)


def help():
    messagebox.showinfo(title="Help", icon="question", message="Need help?")


# set up gui layout
root = tk.Tk()
root.option_add("*tearOff", False)
root.title("rgba: Color Palette!")
root.minsize(500, 300)
mainframe = ttk.Frame(root, padding="3 3")
mainframe.grid(column=0, row=0, sticky=(tk.N, tk.E, tk.S, tk.W))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)


notebook = ttk.Notebook(mainframe)
tab1_img = ttk.Frame(notebook, padding="5 5 5 5")
img_display = ttk.Label(tab1_img, text="No image selected!").grid(column=2, row=1)
tab2_2palette = ttk.Frame(notebook)
tab3_3palette = ttk.Frame(notebook)
tab4_4palette = ttk.Frame(notebook)
tab5_5palette = ttk.Frame(notebook)

notebook.add(tab1_img, text="Selected Image")
notebook.add(tab2_2palette, text="2-Color Palette")
notebook.add(tab3_3palette, text="3-Color Palette")
notebook.add(tab4_4palette, text="4-Color Palette")
notebook.add(tab5_5palette, text="5-Color Palette")
notebook.pack()

'''IF B&W IMG, STATE = DISABLED FOR THE 3-5 PALETTE TAB'''

# create menu and menu items
win = tk.Toplevel(root)
menubar = tk.Menu(win)
win["menu"] = menubar  # configure 'menu' option to attach menu widget to window

menu_file = tk.Menu(menubar)  # File menu
menu_other = tk.Menu(menubar)  # Other menu

menubar.add_cascade(menu=menu_file, label="Open Image")
menu_file.add_command(label="Open from computer...", command=open_file)
menu_file.add_command(label="Open from Image URL...", command=open_url)

menubar.add_cascade(menu=menu_other, label="Other")
menu_other.add_command(label="Help", command=help)
menu_other.add_separator()
menu_other.add_command(label="About", command=about)


def check_file():
    global computer_file
    if computer_file is not None and computer_file != "":
        img_display["image"] = computer_file
        img_display.configure(image=computer_file)

check_file()

root.mainloop()

# palette_list = Image.getpalette(img)
# img_display["image"] = THE IMAGE VARIABLE