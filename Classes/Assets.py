from Classes.Final import *
from Classes.Animated import Animation
from Classes.GameObject import GameObject
import pygame


Assets = {
    "common":{
        "chest": [Chest, {}],
        "ground": [Ground, {}],
        "player": [Player, {}],
        "enemy": [Enemy, {}],
    },
    "dungeon": {
        "d1-c-tl": [Ground, {
            "image_path": "images/nic.png"
        }],
        "d1-c-tr": [Ground, {
            "image_path": "images/nic.png"
        }],
        "d1-c-bl": [Ground, {
            "image_path": "images/nic.png"
        }],
        "d1-c-br": [Ground, {
            "image_path": "images/nic.png"
        }],
        "d1-l-br": [Ground, {
            "image_path": "images/nic.png"
        }],
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
