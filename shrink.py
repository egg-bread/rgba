# =====================
# rgba: Shrink! allows the user to select a folder of images to shrink in dimensions by a percentage of their original size
# and saves a copy of the shrunken images to that same folder!
# =====================

# =====================
# import libraries
# =====================
import glob
import os
from tkinter import *
from tkinter import filedialog
from tkinter import simpledialog
from tkinter import ttk
from tkinter import messagebox
from PIL import Image

# =====================
# where the magic happens
# =====================
# initialize root window
root = Tk()
root.resizable(FALSE, FALSE)

# useful variables
directory = "" # folder location
cur_progress = DoubleVar() # for progress tracking


def open_folder():
    global directory
    directory = filedialog.askdirectory()
    if directory != "":
        status["text"] = "Folder selected."


def shrink_size():
    global directory
    # check if user has not selected a folder location
    if directory is "":
        messagebox.showerror(title="Error!", message="No folder has been selected!")
        return
    else: # a folder location has been selected
        result = check4images() # checks if folder has images
        if result is False:
            return
        else: # folder has images so ask user for resize percentage!
            # ask for percentage reduction in image dimensions
            reduction_percentage = simpledialog.askinteger(title="Reduce All Image Dimensions By...",
                                                           prompt="Enter a whole number for the percentage you wish to"+\
                                                                  " reduce all image's size by:")
            # check to make sure user input is valid: False = not valid, True = valid
            valid_int = check_reduction(reduction_percentage)
            if valid_int is True:
                # ask user for confirmation of reduction_percentage
                ask4confirmation = messagebox.askyesno(title="Confirmation",
                                                       message="Reduce all images' size by {}%?".format(reduction_percentage),
                                                       icon="question")
                if ask4confirmation is True:
                    # do the resizing w/ reduction_percentage if ask4confirmation is yes
                    resize_it(reduction_percentage)
                    # give user confirmation
                    messagebox.showinfo(title="Success!", message="Images have been resized!")
                    cur_progress.set(0)
                    select_button["state"] = ACTIVE
                    resize_button["state"] = ACTIVE
                    status["text"] = "Select a folder."
                    directory = "" # wipe folder location


# check_reduction(p) returns True if p is a whole number between 0-100 not inclusive
def check_reduction(p):
    if p is None:
        return
    elif p == 0:
        messagebox.showerror(title=";-)", message="You entered 0! You sure you need to use this program?")
    elif p < 0:
        messagebox.showerror(title="Error!", message="You didn't enter a valid number!")
    elif p >= 100:
        messagebox.showerror(title="Error!", message="You didn't enter a valid number!")
    else: # user entered a valid reduction % from 0-100 not inclusive
        return True


# check4images() resizes and saves all images to the selected folder (directory)
def check4images():
    global directory
    if glob.glob(directory+"/*.jpg") == [] and glob.glob(directory+"/*.png") == [] and glob.glob(directory+"/*.jpeg") == []:
        messagebox.showerror(title="Uh oh!", message="There are no images in this folder!")
        directory = ""  # wipe folder location
        status["text"] = "Please select a different folder."
        return False


def grab_extensions(dir):
    img_ext = (".png", ".jpeg", ".jpg") # valid image extensions to look for
    extensions = [] # image extensions present in dir files
    for file in glob.glob(dir+"/*"):
        if file.endswith(img_ext):
            # find out what extension it is
            root, ext = os.path.splitext(file) # get extension from path
            if ext not in extensions: # if the image extension has not been added to the extensions list, append it
                extensions.append(ext)
    return extensions


def number_of_images(extensions, dir):
    total = 0
    for ext in extensions:
        for image in glob.glob(dir+"/*"+ext):
            total += 1
    return total


def resize_it(reduce):
    global directory, cur_progress
    loe = grab_extensions(directory) # grab what image extensions are in the folder
    # update status on gui and disable any buttons from being clicked and triggering commands
    status["text"] = "Shrinking image(s)..."
    select_button["state"] = DISABLED
    resize_button["state"] = DISABLED
    progress_step = 100 / number_of_images(loe, directory) # what one "step" on progress is
    for ext in loe:
        if ext == ".png":
            type = "PNG"
        else:
            type = "JPEG"
        for file in glob.glob(directory+"/*"+ext):
            root, ext = os.path.splitext(file) # get extension from path
            img = Image.open(file)
            new_width = img.width * (100-reduce) / 100
            new_height = img.height * (100-reduce) / 100
            resized_img = img.resize((round(new_width), round(new_height)), resample=Image.BICUBIC)
            resized_img.save(root + "_smaller" + ext, type) # saved to same folder with "_smaller" added to the file name
            # update progress
            prev_progress = cur_progress.get()
            cur_progress.set(prev_progress + progress_step)


# =====================
# create gui
# =====================
root.title("rgba: Shrink!")
mainframe = ttk.Frame(root)
mainframe.grid(column=0, row=0, sticky=(N, W, E, S))
mainframe.columnconfigure(0, weight=1)
mainframe.rowconfigure(0, weight=1)

# select folder location button
select_button = ttk.Button(mainframe, text="Open Folder", command=open_folder)
select_button.grid(column=0, row=0, sticky=(S, N, E, W))

# resize all images in that folder button
resize_button = ttk.Button(mainframe, text="Resize Images!", command=shrink_size)
resize_button.grid(column=1, row=0, sticky=(S, N, E, W))

# shows current status of program
status = ttk.Label(mainframe, text="No folder selected.")
status.grid(column=0, row=1, sticky=(S, N, E, W))

# progress bar for saving images
progress = ttk.Progressbar(mainframe, orient=HORIZONTAL, length = 100, mode="determinate", variable=cur_progress)
progress.grid(column=1, row=1)

# add some padding around gui elements so they aren't squished!
for child in mainframe.winfo_children():
    child.grid_configure(padx=5, pady=5)

root.mainloop()

# color profiles are not preserved after resizing if they existed in the first place so slight change in image color
# > Example: Adobe RGB (1998) color profile of an image is removed from the resized image