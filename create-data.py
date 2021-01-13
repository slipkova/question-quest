import PIL
from PIL import Image
import os
import numpy
import json


def flip_image(image):
    for x in range(6):
        im = Image.open(f"assets/test-guy/animation/run/right/r{x + 1}.png")
        out = im.transpose(PIL.Image.FLIP_LEFT_RIGHT)
        out.save(f"assets/animation/test-guy/run/left/l{x+1}.png")


def img_to_anim(**kwargs):
    """kwarks: path, name, length, image_folder"""
    arrs = []
    for file in os.listdir(kwargs["image_folder"]):
        img = Image.open(f'{kwargs["image_folder"]}{"/" if kwargs["image_folder"][-1] != "/" else ""}{file}').convert(mode="RGBA")
        arr = numpy.array(img)
        arrs.append(arr.tolist())

    anim = {
        "duration": kwargs["duration"],
        "colorkey": kwargs["colorkey"],
        "frames": arrs
    }
    with open(f'{kwargs["path"]}{"/" if kwargs["path"][-1] != "/" else ""}{kwargs["name"]}', 'w') as outfile:
        json.dump(anim, outfile)


    """
    for i, arr in enumerate(arrs):
        img = PIL.Image.fromarray(numpy.uint8(arr))
        out = img.transpose(PIL.Image.FLIP_TOP_BOTTOM)
        out.save(f"test/test{i+1}.png")
"""


"""
img_to_anim(image_folder="assets/animation/test-guy/run/right/", path="assets/animation/test-guy/", duration=1, name="run-right.json", colorkey=[0,0,0])
img_to_anim(image_folder="assets/animation/test-guy/run/left/", path="assets/animation/test-guy/", duration=1, name="run-left.json", colorkey=[0,0,0])
img_to_anim(image_folder="assets/animation/test-guy/run/back/", path="assets/animation/test-guy/", duration=1, name="run-top.json", colorkey=[0,0,0])
img_to_anim(image_folder="assets/animation/test-guy/run/front/", path="assets/animation/test-guy/", duration=1, name="run-bottom.json", colorkey=[0,0,0])
"""

img_to_anim(image_folder="assets/blue-enemy/animation/idle/", path="assets/blue-enemy/animation/", duration=1,
            name="idle.json", colorkey=[255,255,255])
