from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser

# function to open the image file
def open_image(canvas, width, height):
    global imageRaw
    file_path = filedialog.askopenfilename(title="Open Image File", filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")])
    if file_path:
        imageRaw = Image.open(file_path)
        
        showImage(canvas, width, height)

def flip_image(canvas, width, height):
    try:
        global imageRaw
        imageRaw = imageRaw.transpose(Image.FLIP_LEFT_RIGHT)
        
        showImage(canvas, width, height)
    except:
        showerror(title='Flip Image Error', message='Please select an image to flip!')

def rotate_image(canvas, width, height):
    try:
        global imageRaw

        imageRaw = imageRaw.rotate(90, expand=True)
        showImage(canvas, width, height)
        
    except:
        showerror(title='Rotate Image Error', message='Please select an image to rotate!')

def showImage(canvas, width, height):
    global imageRaw, imageTk

    image = ImageOps.fit(imageRaw, (width, height), method = 0, bleed = 0.0, centering =(0.5, 0.5)) 
    imageTk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=imageTk)