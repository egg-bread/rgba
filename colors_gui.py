# =====================
# import libraries
# =====================
import requests
from io import BytesIO
from tkinter import *
from tkinter import filedialog
from tkinter import ttk
from tkinter import messagebox
from tkinter import simpledialog
from PIL import Image, ImageTk


# =====================
# where the magic happens
# =====================

# initialize root window
root = Tk()

# useful constants / variables
error_msg = "An error occurred with the image address you entered! :-(\n" +\
            "Make sure to enter the FULL URL with the http/https!\n" +\
            "Please try again."
target_file = ""


# open_file() opens the user selected image from their computer and displays it
def open_file():
    global target_file
    pil_image = Image.open(filedialog.askopenfilename(title="Select an image!")) # opens as a PIL image
    check_transparency(pil_image) # check if alpha composition needs to be done and run image_preview
    image_preview(pil_image) # in case pil_image is not transparent, still need to get smaller image size for display
    display_target() # set image up on display


# opens_url() opens the image from the entered URL (as long as it is valid) and displays it
def open_url():
    global target_file
    get_url = simpledialog.askstring(title="Enter Image URL", prompt="Enter the full image address below!")
    if get_url is None or check_url(get_url) is True:
        return
    default_request = requests.get(get_url)
    initialize = Image.open(BytesIO(default_request.content))
    check_transparency(initialize) # check if alpha composition needs to be done and run image_preview
    image_preview(initialize) # in case initialize is not transparent, still need to get smaller image size for display
    display_target() # set image up on display


def check_transparency(img):
    global target_file
    try:
        # credits to shuuji3 over @ https://stackoverflow.com/questions/9166400/
        # for how to replace transparent parts of an image with white! :D
        bg = Image.new("RGBA", img.size, (255, 255, 255))
        alpha_comp = Image.alpha_composite(bg, img)
        image_preview(alpha_comp)
    except ValueError:
        target_file = ImageTk.PhotoImage(img) # target_file has no transparency as rgba image & is made tkinter-compatible


# image_preview(img) resizes img to a window-proportionate display size if necessary
def image_preview(img):
    global target_file
    orig_h = img.height
    orig_w = img.width
    new_multiplier = min((350/orig_h), (350/orig_w))
    if img.height > 350 or img.width > 350:
        new_h = round(orig_h * new_multiplier)
        new_w = round(orig_w * new_multiplier)
        img.thumbnail((new_w, new_h))
        target_file = ImageTk.PhotoImage(img)
    else:
        target_file = ImageTk.PhotoImage(img)


# check_file() displays target_file if it is a valid image
def display_target():
    global target_file
    if target_file is not None and target_file != "":
        img_display.configure(image=target_file)
        img_display.image = target_file


# check_url checks for any errors in accessing the given image URL including if the entered URL
#           is just an empty string
def check_url(url):
    if url == "":
        messagebox.showerror(title="Oops!", message=error_msg)
        return True
    try:
        requests.get(url)
    except ValueError:
        messagebox.showerror(title="Oops!", message=error_msg)
        return True


# =====================
# set up gui
# =====================
root.title("rgba: Color Palette!")
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# target_file's parent frame
imgframe = ttk.LabelFrame(mainframe, text="Selected Image")
imgframe.grid(column=0, row=1, sticky=W)
# where target_file is displayed
img_display = ttk.Label(imgframe, text="Select an image to get a 4-color palette!")
img_display.grid(column=0, row=0, sticky=(N, E, W))

# palette's parent frame
paletteframe = ttk.LabelFrame(mainframe, text="Color Palette")
paletteframe.grid(column=1, row=1, sticky=E)
# where the color palette is displayed
palette = ttk.Label(paletteframe, text="Your image's color palette will be here...")
palette.grid(sticky=(N, E, W))

# clickable buttons
file_button = ttk.Button(imgframe, text="Open Image from File", command=open_file).grid(column=0, row=1, sticky=S)
url_button = ttk.Button(imgframe, text="Open Image from URL", command=open_url).grid(column=0, row=2, sticky=S)
export_button = ttk.Button(paletteframe, text="Export Palette").grid(sticky=S)

# add some padding around gui elements so they aren't squished!
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

root.mainloop()