from Classes.Final import *
from Classes.Animated import Animation
from Classes.GameObject import GameObject
import pygame
import os


dungeon1 = {}
for img in os.listdir("assets/world/dungeon1/sprites/"):
    if img.startswith("d1-"):
        dungeon1[img.partition(".")[0]] = [Ground, {
            "image_path": f"assets/world/dungeon1/sprites/{img}",
            "colorkey": (0, 0, 0)
        }]


Assets = {
    "common": {
        "chest": [Chest, {}],
        "ground": [Ground, {}],
        "player": [Player, {}],
        "enemy": [Enemy, {}],
        "enter-pad": [EnterPad, {}],
        "exit-pad": [ExitPad, {}],
        "block": [Ground, {
            "image_path": "assets/images/nic.png",
            "dev_image_path": "assets/images/block.png",
            "colorkey": (0, 0, 0),
            "solid": True
        }]
    },
    "dungeon 1": {
        **dungeon1
    }
}


def all_assets():
    all_assets = {}
    for group in Assets.keys():
        for asset in Assets[group].keys():
            all_assets[asset] = Assets[group][asset]
    return all_assets


GameClasses = {
    "animation": Animation,
}
