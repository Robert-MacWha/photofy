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
    global private_key, address, contract_address
    private_key = os.getenv("PRIVATE_KEY")
    address = os.getenv("ADDRESS")
    contract_address = os.getenv("CONTRACT_ADDRESS")

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


def flip_image(canvas, width, height):
    try:
        global imageRaw
        imageRaw = imageRaw.transpose(Image.FLIP_LEFT_RIGHT)

        showImage(canvas, width, height)
    except:
        showerror(title="Flip Image Error", message="Please select an image to flip!")


def rotate_image(canvas, width, height):
    try:
        global imageRaw

        imageRaw = imageRaw.rotate(90, expand=True)
        showImage(canvas, width, height)

    except:
        showerror(
            title="Rotate Image Error", message="Please select an image to rotate!"
        )


def saveImage():
    global imageRaw

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
    print("sha", imageSha)

    w3 = Web3(Web3.HTTPProvider("http://127.0.0.1:8545/"))

    # load contract abi
    compiled_sol = json.load(open("../backend/compiled.json", "r"))
    abi = json.loads(
        compiled_sol["contracts"]["ImageRepository.sol"]["ImageRepository"]["metadata"]
    )["output"]["abi"]

    storage_sol = w3.eth.contract(abi=abi, address=w3.to_checksum_address(contract_address))
    nonce = w3.eth.get_transaction_count(address)

    unsigned_tx = storage_sol.functions.uploadImage(
        priorSha.encode("utf-8")[:32], imageSha.encode("utf-8")[:32], trustScore
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

def computeSha256(img):
    img_data = img.tobytes()
    print([str(x) for x in img_data[20000:20100]])
    sha256_hash = hashlib.sha256(img_data).hexdigest()
    return sha256_hash
