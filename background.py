# =====================
# rgba: Background! replaces transparent parts of a PNG image with the user's selected choice of color. The image
# then can be saved to the user's computer!
# =====================

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
from tkinter import colorchooser
from PIL import Image, ImageTk

# =====================
# where the magic happens
# =====================

# initialize root window
root = Tk()
root.resizable(FALSE, FALSE)

# useful constants / variables
error_msg = "An error occurred with the image address you entered! :-(\n" +\
            "Make sure to enter the FULL URL with the http/https!\n" +\
            "Please try again."
transparent = False

original_png = ""
original_thumb = ""
edited_png = ""

tkinter_png = ""

png_loaded = False

types = [("PNG Images", "*.png")] # file types allowed for platforms that have this option


# open_file() opens the user selected image from their computer and displays it
def open_file():
    global edited_png
    global transparent, original_png, original_thumb
    original_png = Image.open(filedialog.askopenfilename(title="Select an image!", filetypes=types)) # opens as a PIL image
    original_thumb = original_png.copy() # create a copy of the orig image for display & editing purposes
    if not isinstance(edited_png, str): # wiping previous loaded image's edited image
        edited_png = ""
    # check if png is Palette (P) mode which requires converting into RGBA mode
    if original_png.mode is "P":
        original_png = original_png.convert(mode="RGBA")
    check_transparency(original_png)
    if transparent is True:
        bg = Image.new("RGBA", original_png.size, (255, 255, 255))
        original_thumb = Image.alpha_composite(bg, original_png)
        image_preview()
        display_target()
        transparent = False # switch transparent to False in case user wants to select a new image


# opens_url() opens the PNG from the entered URL (as long as it is valid) and displays it
def open_url():
    global transparent, original_png, original_thumb, edited_png
    get_url = simpledialog.askstring(title="Enter Image URL", prompt="Enter the full image address below!")
    if get_url is None or check_url(get_url) is True:
        return
    default_request = requests.get(get_url)
    original_png = Image.open(BytesIO(default_request.content))
    original_thumb = original_png.copy()
    if not isinstance(edited_png, str): # wiping previous loaded image's edited image
        edited_png = ""
    # check if png is Palette (P) mode which requires converting into RGBA mode
    if original_png.mode is "P":
        original_png = original_png.convert(mode="RGBA")
    check_transparency(original_png)
    if transparent is True:
        bg = Image.new("RGBA", original_png.size, (255, 255, 255))
        original_thumb = Image.alpha_composite(bg, original_png)
        image_preview()
        display_target()
        transparent = False # switch transparent to False in case user wants to select a new image


# check_transparency(png) checks if img contains transparency; if it does, make the transparent parts white
def check_transparency(png):
    global transparent
    try:
        # credits to shuuji3 over @ https://stackoverflow.com/questions/9166400/
        # for how to replace transparent parts of an image with a color! :D
        bg = Image.new("RGBA", png.size, (255, 255, 255))
        alpha_comp = Image.alpha_composite(bg, png)
       # print("Apparently transparent")
        transparent = True
    except ValueError:
       # print("Not transparent")
        not_transparent()


# not_transparent() shows a popup dialogue notifying the user that their image contains no transparency
def not_transparent():
    messagebox.showerror(title="Uh oh...", message="Your image contains no transparent parts :(")


# image_preview() resizes original_thumb to a window-proportionate display size if necessary
def image_preview():
    global original_thumb, tkinter_png
    # get original's image dimensions
    orig_h = original_thumb.height
    orig_w = original_thumb.width
    new_multiplier = min((500/orig_h), (500/orig_w))
    if original_thumb.height > 500 or original_thumb.width > 500:
        new_h = round(orig_h * new_multiplier)
        new_w = round(orig_w * new_multiplier)
        original_thumb.thumbnail((new_w, new_h))
        tkinter_png = ImageTk.PhotoImage(original_thumb)
    else:
        tkinter_png = ImageTk.PhotoImage(original_thumb)


# display_target() displays the image on the GUI
def display_target():
    global tkinter_png, png_loaded
    if original_png is not None and tkinter_png != "":
        png_display.configure(image=tkinter_png)
        png_display.image = tkinter_png
        png_loaded = True


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


# save_new_png() saves the edited image to user selected directory and name
def save_new_png():
    if png_loaded is False: # user has not selected an image so not possible to save the "new" image
        messagebox.showerror(title="Oops!", message="Nice try but no PNG has been selected!")
    else:
        savefilename = filedialog.asksaveasfilename()
        if len(savefilename) == 0:
            return
        elif isinstance(edited_png, str):
            # save original_png as user did not make any bg changes so edited_png is still an empty string
            original_png.save(savefilename+".png", format="PNG")
            messagebox.showinfo(title="Woohoo!", message="Your beautiful PNG has been saved even though you made no"+\
                                " background color changes!")
        else:
            # save edited_png
            edited_png.save(savefilename+".png", "PNG")
            messagebox.showinfo(title="Woohoo!", message="Your beautiful PNG has been saved!")


# select_bg_color() asks the user for the background color they want their image to have and displays a preview of their
#                   new image
def select_bg_color():
    global original_thumb, edited_png
    picked = colorchooser.askcolor()
    rgb = (int(picked[0][0]), int(picked[0][1]), int(picked[0][2]))
    if png_loaded is False: # user has not selected an image so not possible to apply the bg color to the image
        messagebox.showerror(title="Oops!", message="Nice try but no PNG has been selected!")
    else:
        bg = Image.new("RGBA", original_png.size, rgb)
        edited_png = Image.alpha_composite(bg, original_png)
        original_thumb = Image.alpha_composite(bg, original_png)
        image_preview()
        display_target()
        messagebox.showinfo(title="Looking Good!", message="Image background has been updated!")


# =====================
# set up gui
# =====================
root.title("rgba: Background!")
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# where original_png and edited_png are displayed
png_display = ttk.Label(mainframe, text="Waiting for you to open a transparent image...")
png_display.grid(column=1, row=1, sticky=(S, N, E, W))

# clickable buttons
file_button = ttk.Button(mainframe, text="Open PNG from File", command=open_file)
file_button.grid(column=0, row=0, sticky=(S, N, E, W))

url_button = ttk.Button(mainframe, text="Open PNG from URL", command=open_url)
url_button.grid(column=2, row=0, sticky=(S, N, E, W))

bg_button = ttk.Button(mainframe, text="Select Background Color", command=select_bg_color)
bg_button.grid(column=0, row=3, sticky=(S, N, E, W))

export_button = ttk.Button(mainframe, text="Export Image!", command=save_new_png)
export_button.grid(column=2, row=3, sticky=(S, N, E, W))
export_button.bind("<Enter>", lambda e: export_button.configure(text= "Enter save name without .png!"))
export_button.bind("<Leave>", lambda e: export_button.configure(text= "Export Image!"))

# add some padding around gui elements so they aren't squished!
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=5)

root.mainloop()