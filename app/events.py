from tkinter import filedialog
from PIL import Image, ImageOps, ImageTk, ImageFilter, ImageGrab
from tkinter.messagebox import showerror, askyesno
from tkinter import colorchooser

import os
import json
from dotenv import load_dotenv
from web3 import Web3
import hashlib


def on_start() -> tuple:
    load_dotenv()
    global private_key, address, contract_address, pen_color, priorSha
    
    private_key = os.getenv("PRIVATE_KEY")
    address = os.getenv("ADDRESS")
    contract_address = os.getenv("CONTRACT_ADDRESS")
    pen_color = "#000000"
    priorSha = 0

    if private_key == None:
        w3 = Web3()
        acc = w3.eth.account.create()
        aHex = w3.to_hex(acc._private_key)

        private_key = str(aHex)
        address = acc.address

        with open(".env", "a+") as f:
            f.write(f"PRIVATE_KEY={private_key}\n")
            f.write(f"ADDRESS={address}\n")

    return address, private_key


# function to open the image file
def open_image(canvas, width, height):
    global priorSha, imageRaw, trustScore
    trustScore = 0

    file_path = filedialog.askopenfilename(
        title="Open Image File",
        filetypes=[("Image Files", "*.jpg;*.jpeg;*.png;*.gif;*.bmp")],
    )
    if file_path:
        imageRaw = Image.open(file_path)
        priorSha = computeSha256(imageRaw)

        showImage(canvas, width, height)
        uploadImage()


def flip_image(canvas, width, height):
    global imageRaw, trustScore
    trustScore = max(trustScore, 10)
    
    imageRaw = imageRaw.transpose(Image.FLIP_LEFT_RIGHT)
    showImage(canvas, width, height)


def rotate_image(canvas, width, height):
    global imageRaw, trustScore
    trustScore = max(trustScore, 10)

    imageRaw = imageRaw.rotate(90, expand=True)
    showImage(canvas, width, height)

def applyFilter(filter, canvas, width, height):
    global imageRaw, imageTk, trustScore
    trustScore = max(trustScore, 15)

    # apply the filter to the rotated image
    if filter == "Black and White":
        imageRaw = ImageOps.grayscale(imageRaw)
    elif filter == "Blur":
        imageRaw = imageRaw.filter(ImageFilter.BLUR)
    elif filter == "Contour":
        imageRaw = imageRaw.filter(ImageFilter.CONTOUR)
    elif filter == "Detail":
        imageRaw = imageRaw.filter(ImageFilter.DETAIL)
    elif filter == "Emboss":
        imageRaw = imageRaw.filter(ImageFilter.EMBOSS)
    elif filter == "Edge Enhance":
        imageRaw = imageRaw.filter(ImageFilter.EDGE_ENHANCE)
    elif filter == "Sharpen":
        imageRaw = imageRaw.filter(ImageFilter.SHARPEN)
    elif filter == "Smooth":
        imageRaw = imageRaw.filter(ImageFilter.SMOOTH)        

    showImage(canvas, width, height)

# function for drawing lines on the opened image
def draw(event, canvas):
    global pen_color, trustScore
    trustScore = max(trustScore, 100)

    pen_size = 10
    x1, y1 = (event.x - pen_size), (event.y - pen_size)
    x2, y2 = (event.x + pen_size), (event.y + pen_size)
    canvas.create_oval(x1, y1, x2, y2, fill=pen_color, outline="", width=pen_size, tags="oval")

def changeColor():
    global pen_color
    pen_color = colorchooser.askcolor(title="Select Pen Color")[1]

def eraseLines(canvas):
    canvas.delete("oval")

def saveImage(canvas):
    global imageRaw

    imageRaw = ImageGrab.grab(bbox=(canvas.winfo_rootx(), canvas.winfo_rooty(), canvas.winfo_rootx() + canvas.winfo_width(), canvas.winfo_rooty() + canvas.winfo_height()))

    uploadImage()

    file_path = filedialog.asksaveasfilename(defaultextension=".jpg")
    if file_path:
        imageRaw.save(file_path)


def showImage(canvas, width, height):
    global imageRaw, imageTk

    image = ImageOps.fit(
        imageRaw, (width, height), method=0, bleed=0.0, centering=(0.5, 0.5)
    )
    imageTk = ImageTk.PhotoImage(image)
    canvas.create_image(0, 0, anchor="nw", image=imageTk)


def uploadImage():
    global priorSha, imageRaw, private_key, address, contract_address

    imageSha = computeSha256(imageRaw)
    print("Hash:", imageSha, priorSha)

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))

    # load contract abi
    compiled_sol = json.load(open("../backend/compiled.json", "r"))
    abi = json.loads(
        compiled_sol["contracts"]["ImageRepository.sol"]["ImageRepository"]["metadata"]
    )["output"]["abi"]

    storage_sol = w3.eth.contract(abi=abi, address=w3.to_checksum_address(contract_address))
    nonce = w3.eth.get_transaction_count(address)

    print("Trust -------------------------------", trustScore)
    unsigned_tx = storage_sol.functions.uploadImage(
        bytes.fromhex(priorSha), bytes.fromhex(imageSha), trustScore
    ).build_transaction(
        {
            "from": address,
            "nonce": nonce
        }
    )
    signed_tx = w3.eth.account.sign_transaction(unsigned_tx, private_key=private_key)

    tx_hash = w3.eth.send_raw_transaction(signed_tx.rawTransaction)
    w3.eth.wait_for_transaction_receipt(tx_hash)

    priorSha = imageSha

def uploadWithWorldcoin():
    # TODO
    pass

def computeSha256(img: Image.Image):
    img_data = img.copy().convert("RGBA").tobytes()
    sha256_hash = hashlib.sha256(img_data).hexdigest()
    return sha256_hash
