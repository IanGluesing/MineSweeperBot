import numpy as np
import cv2
from PIL import ImageGrab, Image, ImageMath
import pyautogui
import time
import random



def setUpGame():
    ans = input("What difficulty are you playing on(easy,medium,hard)")
    if ans == "easy":
        easy_coords = [247, 401, 696, 760]  # 10x8, 45 pixels thick
        width = 9
        height = 8
        spacing = 45
        return easy_coords, width, height, spacing
    elif ans == "medium":
        medium_coords = [202, 371, 741, 790]  # 18x14, 30 pixels thick
        width = 17
        height = 14
        spacing = 30
        return medium_coords, width, height, spacing
    elif ans == "hard":
        hard_coords = [172, 331, 771, 830]  # 24x20,
        width = 23
        height = 21
        spacing = 25
        return hard_coords, width, height, spacing


# Coordinates of the game using googles built in minesweeper game


def startGame():

    coords, width, height, spacing = setUpGame()

    # screen = np.array(ImageGrab.grab(bbox=coords))
    # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    pyautogui.moveTo(random.randrange(coords[0], coords[2]),random.randrange(coords[1],coords[3]))
    pyautogui.click()

    pyautogui.moveTo(coords[0] + (spacing/2),coords[1] + (spacing/2))

    for i in range(height):
        for j in range(width):
            pyautogui.move(spacing, 0)
            #time.sleep(.2)
            x,y = pyautogui.position()
            pixelColor = pyautogui.screenshot().getpixel((x,y))
            # print(pixelColor)
            if(pixelColor == (211, 47, 47)):
                print("red")
        pyautogui.move(-width * spacing, spacing)



startGame()



# go through each box of the game and figure out its number