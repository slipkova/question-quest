import PIL
from PIL import Image
import os
import numpy
import json
from tkinter import Tk
from tkinter import filedialog, simpledialog


def open_path(title):
    return filedialog.askdirectory(initialdir=os.getcwd(), title=title)

def split_image(**kwargs):
    im = numpy.array(Image.open(kwargs["image_path"]).convert(mode="RGBA"))
    tiles = [im[x:x + kwargs["segments"], y:y + kwargs["segments"]].tolist() for x in range(0, im.shape[0], kwargs["segments"])
             for y in range(0, im.shape[1], kwargs["segments"])]
    if kwargs["name"].startswith("close"):
        tiles.reverse()
    anim = {
        "duration": kwargs["duration"],
        "colorkey": kwargs["colorkey"],
        "frames": tiles
    }
    with open(f'{kwargs["path"]}{"/" if kwargs["path"][-1] != "/" else ""}{kwargs["name"]}', 'w') as outfile:
        json.dump(anim, outfile)


root = Tk()
split_image(image_path=filedialog.askopenfilename(initialdir=os.getcwd(),
                                                  title="Select image to slice",
                                                  filetypes=(("images", "*.png"),
                                                             ("all files", "*.*"))),
            segments=simpledialog.askinteger("", "Segment size:"),
            path=open_path("Select folder save animation"),
            duration=simpledialog.askfloat("", "Enter animation duration:"),
            name=simpledialog.askstring("", "Enter animation name:"),
            colorkey=(simpledialog.askinteger("", "Enter animation colorkey r:"), simpledialog.askinteger("", "Enter animation colorkey g:"), simpledialog.askinteger("", "Enter animation colorkey b:"))
            )
root.quit()
