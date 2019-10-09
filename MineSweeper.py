import numpy as np
import cv2
from PIL import ImageGrab, Image, ImageMath
import pyautogui
import time
import random


# (185, 221, 119)
# (191, 225, 125) 2 boxes that dont have numbers in them


def setUpGame():
    ans = input("What difficulty are you playing on(easy,medium,hard)")
    if ans == "easy":
        easy_coords = [247, 401, 696, 760]  # 10x8, 45 pixels thick
        width = 9
        height = 8
        spacing = 45
        biasX = 2
        biasY = 12
        return easy_coords, width, height, spacing, biasX, biasY
    elif ans == "medium":
        medium_coords = [202, 371, 741, 790]  # 18x14, 30 pixels thick
        width = 17
        height = 14
        spacing = 30
        biasX = 1
        biasY = 7
        return medium_coords, width, height, spacing, biasX, biasY
    elif ans == "hard":
        hard_coords = [172, 331, 771, 830]  # 24x20,
        width = 23
        height = 20
        spacing = 25
        biasX = 1
        biasY = 4.5# 7 pretty good
        return hard_coords, width, height, spacing, biasX, biasY


# Coordinates of the game using googles built in minesweeper game


def startGame():

    coords, width, height, spacing, biasX, biasY = setUpGame()

    # screen = np.array(ImageGrab.grab(bbox=coords))
    # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    pyautogui.moveTo(random.randrange(coords[0], coords[2]),random.randrange(coords[1],coords[3]))
    pyautogui.click()

    pyautogui.moveTo(coords[0] + (spacing/2) + biasX,coords[1] + (spacing/2) + biasY)

    for i in range(height):
        for j in range(width):
            pyautogui.move(spacing, 0)
            doCalculations(spacing)
            # send pixel color to method that does something with it

        pyautogui.move(-width * spacing, spacing)
        doCalculations(spacing)


def doCalculations(spacing):
    # [(1),(2),(3),(4),....]
    possibleColors = [(25, 118, 210),(56, 142, 60),(211, 47, 47),(123, 31, 162),(255,143,0)]
    # add up values of the incoming color and see if they are in a certain range
    # and then based on that number do stuff
    # time.sleep(.2)
    x, y = pyautogui.position()
    pixelColor = pyautogui.screenshot().getpixel((x, y))
    if pixelColor in possibleColors:
        flagNeighbors(possibleColors.index(pixelColor) + 1, spacing)

def flagNeighbors(blockNumber, spacing):
    origX,origY = pyautogui.position()
    movePairs = [(0, -spacing),(spacing, 0),(0,spacing),(0,spacing),(-spacing,0),(-spacing,0),
                 (0,-spacing),(0,-spacing),(spacing,spacing)]
    greenSquares = [(185,221,119),(191,225,125)]
    greenAmt = 0
    redAmt = 0
    pyautogui.move(-10,-12)
    for pair in movePairs:
        pyautogui.move(pair[0],pair[1])
        x, y = pyautogui.position()
        pixelColor = pyautogui.screenshot().getpixel((x, y))
        if pixelColor in greenSquares:
            greenAmt += 1
        if pixelColor == (242, 54, 7):
            redAmt += 1
    if (redAmt + greenAmt) <= blockNumber and redAmt != blockNumber:
        for pair in movePairs:
            pyautogui.move(pair[0], pair[1])
            x, y = pyautogui.position()
            pixelColor = pyautogui.screenshot().getpixel((x, y))
            if pixelColor in greenSquares:
                pyautogui.click(button='right')
    pyautogui.moveTo(origX,origY)



startGame()



# go through each box of the game and figure out its number