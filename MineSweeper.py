import numpy as np
import cv2
from PIL import ImageGrab, Image, ImageMath
import pyautogui
import time
import random


# (185, 221, 119)
# (191, 225, 125) 2 boxes that dont have numbers in them
screenShot = 0
x = 0
y = 0

def setUpGame():
    ans = input("What difficulty are you playing on(easy,medium,hard)")
    if ans == "easy":
        easy_coords = [247, 401, 696, 760]  # 10x8, 45 pixels thick
        width = 9
        height = 8
        spacing = 45
        biasX = 2
        biasY = 12
        redFlag = [-10,-12]
        return easy_coords, width, height, spacing, biasX, biasY, redFlag
    elif ans == "medium":
        medium_coords = [202, 371, 741, 790]  # 18x14, 30 pixels thick
        width = 17
        height = 14
        spacing = 30
        biasX = 1
        biasY = 7
        redFlag = [-8, -12]
        return medium_coords, width, height, spacing, biasX, biasY, redFlag
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
    global screenShot, x, y
    coords, width, height, spacing, biasX, biasY, redFlag = setUpGame()

    # screen = np.array(ImageGrab.grab(bbox=coords))
    # screen = cv2.cvtColor(screen, cv2.COLOR_BGR2GRAY)

    pyautogui.moveTo(random.randrange(coords[0] + 100, coords[2] - 100),
                     random.randrange(coords[1] + 100,coords[3] - 100))
    pyautogui.click()
    time.sleep(3)

    x = coords[0] + (spacing/2) + biasX
    y = coords[1] + (spacing/2) + biasY
    screenShot = pyautogui.screenshot()
    doCalculations(spacing, redFlag)
    for i in range(height):
        for j in range(width):
            x += spacing
            y += 0
            doCalculations(spacing, redFlag)
            # send pixel color to method that does something with it

        x += -width * spacing
        y += spacing
        doCalculations(spacing, redFlag)


def doCalculations(spacing, redFlag):
    global screenShot, x, y
    # [(1),(2),(3),(4),....]
    possibleColors = [(25, 118, 210),(56, 142, 60),(211, 47, 47),(123, 31, 162),(255,143,0)]
    # add up values of the incoming color and see if they are in a certain range
    # and then based on that number do stuff
    pixelColor = screenShot.getpixel((x, y))
    if pixelColor in possibleColors:
        flagNeighbors(possibleColors.index(pixelColor) + 1, spacing, redFlag)


def flagNeighbors(blockNumber, spacing, redFlag):
    global screenShot, x, y

    origX,origY = x, y

    movePairs = [(-spacing,-spacing),(spacing, 0),(spacing, 0),(0,spacing),(0,spacing),
                 (-spacing,0),(-spacing,0),(0,-spacing),(spacing,0)]
    greenSquares, redSquares = [(162, 209, 73),(170, 215, 81)], [(230,51,7),(242, 54, 7)]

    greenAmt, redAmt = 0,0

    x += redFlag[0]
    y += redFlag[1]
    for pair in movePairs:
        x += pair[0]
        y += pair[1]
        pixelColor = screenShot.getpixel((x, y))
        if pixelColor in greenSquares:
            greenAmt += 1
        if pixelColor in redSquares:
            redAmt += 1
            if redAmt == blockNumber:
                break
        if greenAmt > blockNumber or greenAmt + redAmt > blockNumber:
            x, y = origX, origY
            return
    rightClicks = 0
    if (redAmt + greenAmt) <= blockNumber and redAmt != blockNumber:
        for pair in movePairs:
            x += pair[0]
            y += pair[1]
            pixelColor = screenShot.getpixel((x, y))
            if pixelColor in greenSquares:
                pyautogui.moveTo(x,y)
                pyautogui.click(button='right')
                # pyautogui.moveTo(10,10)
                time.sleep(.3)
                screenShot = pyautogui.screenshot()
                rightClicks += 1
            if rightClicks == greenAmt:
                break
    x, y, = origX, origY

    #Everything above here is for flagging neaighbors if they should be flagged









startGame()



# go through each box of the game and figure out its number