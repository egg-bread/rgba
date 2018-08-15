# =====================
# rgba: Color Palette! produces a 4-color palette* based on the colors that occur most frequently
# on the user-selected JPEG/PNG image. The color palette can be exported as a .txt file with rgb and hex values!
# * if the image is black & white the palette will only produce black & white.
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
from PIL import Image, ImageTk
import copy

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
target_file = ""
transparent = False
image_loaded = False

the_palette = []
hex_canvas = []

rgba_colors = []
rgb_export = []
hex_export = []


# rgb2hexa(triplet) converts triplet, an rgb value, into a hexadecimal
def rgb2hexa(triplet):
    return "#{:02x}{:02x}{:02x}".format(triplet[0], triplet[1], triplet[2])


# open_file() opens the user selected image from their computer and displays it
def open_file():
    global target_file
    global transparent
    global the_palette
    pil_image = Image.open(filedialog.askopenfilename(title="Select an image!")) # opens as a PIL image
    get_colors(pil_image) # grab color data
    check_transparency(pil_image) # also run image_preview if image is transparent
    if transparent is False:
        image_preview(pil_image) # in case pil_image is not transparent, still need to get smaller image size for display
    elif transparent is True:
        transparent = False
    display_target() # set image up on display
    rgb_and_hex_ready(the_palette)


# opens_url() opens the image from the entered URL (as long as it is valid) and displays it
def open_url():
    global target_file
    global transparent
    global the_palette
    get_url = simpledialog.askstring(title="Enter Image URL", prompt="Enter the full image address below!")
    if get_url is None or check_url(get_url) is True:
        return
    default_request = requests.get(get_url)
    opened_from_url = Image.open(BytesIO(default_request.content))
    get_colors(opened_from_url) # grab color data
    check_transparency(opened_from_url) # also run image_preview if image is transparent
    if transparent is False:
        image_preview(opened_from_url) # in case opened_from_url is not transparent, still need to get smaller image size for display
    elif transparent is True:
        transparent = False
    display_target() # set image up on display
    rgb_and_hex_ready(the_palette)


# check_transparency(img) checks if img contains transparency; if it does, make the transparent parts white
def check_transparency(img):
    global target_file
    global transparent
    try:
        # credits to shuuji3 over @ https://stackoverflow.com/questions/9166400/
        # for how to replace transparent parts of an image with white! :D
        bg = Image.new("RGBA", img.size, (255, 255, 255))
        alpha_comp = Image.alpha_composite(bg, img)
        transparent = True
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


# display_target() displays target_file if it is a valid image
def display_target():
    global target_file
    global image_loaded
    if target_file is not None and target_file != "":
        img_display.configure(image=target_file)
        img_display.image = target_file
        image_loaded = True
        palette_preview()


# palette_preview() updates palette_canvas to display the image's palette
def palette_preview():
    global hex_canvas
    for c in hex_canvas:
        palette_canvas.configure(background="#ffffff")


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


# get_colors(img) retrieves all pixels in img and their colors and puts the colors in a list or dictionary
def get_colors(img):
    if img.getcolors() is None: # img contains more than 256 colors
        colors_dict = {}
        width_x = img.width
        height_y = img.height
        for x in range(width_x):
            for y in range(height_y):
                pixel = img.getpixel((x,y))
                if pixel not in colors_dict:
                    colors_dict[pixel] = 0
                    colors_dict[pixel] += 1
                else:
                    colors_dict[pixel] += 1
        get_palette(colors_dict)
    else:
        colors = img.getcolors()
        get_palette(colors)


# get_palette(colors) creates the 4 color palette* using items in colors that appear the most frequently
def get_palette(colors):
    global the_palette
    if isinstance(colors, list): # it's a list of tuple tuples
        dictionary_colors = dict(colors) # convert to a dictionary for easier key-value pair access
        while len(dictionary_colors) > 1:
            if len(the_palette) == 4: # palette is full
                return # CHECK!
            else: # palette is not full
                the_palette.append(dictionary_colors[max(dictionary_colors)])
                del dictionary_colors[max(dictionary_colors)]
    elif isinstance(colors, dict): # it's a dictionary
        dictionary_colors_kv_swap = {val: key for key, val in colors.items()} # create a new dictionary w/ swapped key-value pairs
        while len(dictionary_colors_kv_swap) > 1:
            if len(the_palette) == 4: # palette is full
                return
            else: # palette is not full
                the_palette.append(dictionary_colors_kv_swap[max(dictionary_colors_kv_swap)])
                del dictionary_colors_kv_swap[max(dictionary_colors_kv_swap)]


# save_palette() asks the user where to save the palette IF an image has been selected
def save_palette():
    global image_loaded
    global the_palette
    if image_loaded is False: # user has not selected an image so no palette is possible
        messagebox.showerror(title="Oops!", message="Nice try but no image has been selected!")
    else:
        savefilename = filedialog.asksaveasfilename()
        if len(savefilename) == 0:
            return
        write_palette(savefilename)


# rgb_and_hex_ready(pal) prepares the pal(ette) for export and also displaying a preview of the colors
def rgb_and_hex_ready(pal):
    global hex_canvas
    global rgba_colors
    global rgb_export
    global hex_export
    for col in pal: # makes sure alpha channel (if it exists) is not included in rgb final output
        rgba_colors.append(col[:3])
        rgb_export.append(col[:3])
    for color in rgba_colors:
        while rgb_export.count(color) >= 2: # removes any duplicate rgb colors due to different alpha values in rgba
            rgb_export.remove(color)
    for rgb in rgb_export:
        hex_export.append(rgb2hexa(rgb)) # convert rgb values to hex
    hex_canvas = copy.deepcopy(hex_export)


# write_palette(location) writes the palette colors to a .txt file at location
def write_palette(location):
    global rgb_export
    global hex_export
    with open(location+".txt", "w") as file:
        file.write("Your Image's Color Palette!\n")
        file.write("\nRGB Values:\n")
        for rgb_c in rgb_export:
            file.write("{}\n".format(rgb_c))
        file.write("\nHex Values:\n")
        for hex_c in hex_export:
            file.write("{}\n".format(hex_c))
    messagebox.showinfo(title="Woohoo!", message="Your palette has been saved!")


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
paletteframe = ttk.LabelFrame(mainframe, text="Color Palette Preview")
paletteframe.grid(column=1, row=1, sticky=E)
# where the color palette is displayed
palette_canvas = Canvas(paletteframe, background="#ffffff")
palette_canvas.grid(sticky=N)

# clickable buttons
file_button = ttk.Button(imgframe, text="Open Image from File", command=open_file)
file_button.grid(column=0, row=1, sticky=S)
url_button = ttk.Button(imgframe, text="Open Image from URL", command=open_url)
url_button.grid(column=0, row=2, sticky=S)
export_button = ttk.Button(paletteframe, text="Export Palette!", command=save_palette)
export_button.grid(sticky=S)
export_button.bind("<Enter>", lambda e: export_button.configure(text= "Enter save name without .txt extension"))
export_button.bind("<Leave>", lambda e: export_button.configure(text= "Export Palette!"))

# add some padding around gui elements so they aren't squished!
for child in mainframe.winfo_children():
    child.grid_configure(padx=10, pady=10)

root.mainloop()