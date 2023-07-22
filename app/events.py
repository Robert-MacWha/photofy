from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser

import os
from dotenv import load_dotenv
from web3 import Web3

def on_start() -> tuple:
    load_dotenv()
    private_key = os.getenv("PRIVATE_KEY")
    address = os.getenv("ADDRESS")

    if private_key == None:
        w3 = Web3()
        acc = w3.eth.account.create()
        aHex = w3.to_hex(acc._private_key)

        private_key = str(aHex)
        address = acc.address

        with open(".env", "a+") as f:
            f.write(f"PRIVATE_KEY={private_key}\n")
            f.write(f"ADDRESS={address}\n")

    print(address)
    return address, private_key

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

def saveImage():
    global imageRaw

    file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
    if file_path:
        imageRaw.save(file_path)


def showImage(canvas, width, height):
    global imageRaw, imageTk

    image = ImageOps.fit(imageRaw, (width, height), method = 0, bleed = 0.0, centering =(0.5, 0.5)) 
    imageTk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=imageTk)
