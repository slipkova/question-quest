from Classes.Final import *
from Classes.Animated import Animation
from Classes.GameObject import GameObject
import pygame
import os

dynamic_data = {}


def assign_data(**kwargs):
    if kwargs["init"]:
        dynamic_data[kwargs["tab"]] = {}
    for img in os.listdir(kwargs["path"]):
        if img.endswith(".png"):
            if kwargs["condition"](img):
                dynamic_data[kwargs["tab"]][img.partition(".")[0]] = [kwargs["attrs"][0],
                    {x: (y.replace("xyz", img) if type(y) == str else y) for x, y in kwargs["attrs"][1].items()}]

assign_data(
    tab="dungeon 1", init=True,
    path="assets/world/dungeon1/sprites/",
    condition=lambda a: a.startswith("d1-"),
    attrs=[Ground, {
            "image_path": "assets/world/dungeon1/sprites/xyz",
            "colorkey": (0, 0, 0)}]
)

dynamic_data["dungeon 1"]["d1-door-bl"] = [Door, {
            "image_path": "assets/world/door/2/door.png",
            "animations_folder": "assets/world/door/2/animation/"
}]
dynamic_data["dungeon 1"]["d1-door-bl2"] = [Door, {
            "image_path": "assets/world/door/2/roof/door.png",
            "animations_folder": "assets/world/door/2/roof/animation/"
}]


assign_data(
    tab="land", init=True,
    path="assets/world/path-water",
    condition=lambda a: a.startswith("pp_"),
    attrs=[Ground, {
            "image_path": f"assets/world/path-water/xyz"}])
assign_data(
    tab="hills", init=True,
    path="assets/world/hills",
    condition=lambda a: True,
    attrs=[Ground, {
            "image_path": f"assets/world/hills/xyz"}])
assign_data(
    tab="water", init=True,
    path="assets/world/path-water",
    condition=lambda a: a.startswith("w_"),
    attrs=[Ground, {
            "image_path": f"assets/world/path-water/xyz"}])
assign_data(
    tab="bridge", init=True,
    path="assets/world/path-water",
    condition=lambda a: a.startswith("ppw_"),
    attrs=[Ground, {
            "image_path": f"assets/world/path-water/xyz"}])
assign_data(
    tab="village&trees", init=True,
    path="assets/world/village",
    condition=lambda a: a.startswith("vp-"),
    attrs=[Ground, {
            "image_path": f"assets/world/village/xyz"}])
assign_data(
    tab="village&trees", init=True,
    path="assets/world/village",
    condition=lambda a: a.startswith("vp-"),
    attrs=[Ground, {
            "image_path": f"assets/world/village/xyz"}])
dynamic_data["village&trees"]["door"] = [Door, {
            "image_path": "assets/world/door/3/door.png",
            "animations_folder": "assets/world/door/3/animation/"
}]
assign_data(
    tab="decorations", init=True,
    path="assets/world/village",
    condition=lambda a: a.startswith("dec-"),
    attrs=[Ground, {
            "image_path": f"assets/world/village/xyz"}])
assign_data(
    tab="props", init=True,
    path="assets/world/props/sprites/",
    condition=lambda a: True,
    attrs=[Ground, {
            "image_path": f"assets/world/props/sprites/xyz",
            "colorkey": (0, 0, 0)}])
assign_data(
    tab="effects", init=True,
    path="assets/world/door/light/",
    condition=lambda a: True,
    attrs=[Ground, {
            "image_path": f"assets/world/door/light/xyz",
            "colorkey": (0, 0, 0)}])



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
    **dynamic_data
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
