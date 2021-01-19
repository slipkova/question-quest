import PIL
from PIL import Image
import os
import numpy
import json
from tkinter import Tk
from tkinter import filedialog, simpledialog


def open_path(title):
    return filedialog.askdirectory(initialdir=os.getcwd(), title=title)


def flip_image(image):
    for x in range(6):
        im = Image.open(f"assets/test-guy/animation/run/right/r{x + 1}.png")
        out = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        out.save(f"assets/animation/test-guy/run/left/l{x + 1}.png")


def img_to_anim(**kwargs):
    """kwarks: path, name, length, image_folder"""
    arrs = []
    for file in os.listdir(kwargs["image_folder"]):
        if file.endswith(".png"):
            img = Image.open(
                f'{kwargs["image_folder"]}{"/" if kwargs["image_folder"][-1] != "/" else ""}{file}').convert(mode="RGBA")

            arr = numpy.array(img)
            arrs.append(arr.tolist())

    anim = {
        "duration": kwargs["duration"],
        "colorkey": kwargs["colorkey"],
        "frames": arrs
    }
    with open(f'{kwargs["path"]}{"/" if kwargs["path"][-1] != "/" else ""}{kwargs["name"]}', 'w') as outfile:
        json.dump(anim, outfile)


root = Tk()
img_to_anim(image_folder=open_path("Select folder with images"),
            path=open_path("Select folder save animation"),
            duration=simpledialog.askfloat("", "Enter animation duration:"),
            name=simpledialog.askstring("", "Enter animation name:"),
            colorkey=(simpledialog.askinteger("", "Enter animation colorkey r:"), simpledialog.askinteger("", "Enter animation colorkey g:"), simpledialog.askinteger("", "Enter animation colorkey b:"))
            )
root.quit()
