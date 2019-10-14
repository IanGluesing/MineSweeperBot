import numpy as np
import cv2
from PIL import ImageGrab, Image, ImageMath
import pyautogui
import time
import random

screenShot = 0
click = False
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
        unStuck = [7, 15]
        return easy_coords, width, height, spacing, biasX, biasY, redFlag, unStuck
    elif ans == "medium":
        medium_coords = [202, 371, 741, 790]  # 18x14, 30 pixels thick
        width = 17
        height = 14
        spacing = 30
        biasX = 1
        biasY = 7
        redFlag = [-8, -12]
        unStuck = [5,10]
        return medium_coords, width, height, spacing, biasX, biasY, redFlag, unStuck
    elif ans == "hard":# Not Working
        hard_coords = [172, 331, 771, 830]  # 24x20,
        width = 23
        height = 20
        spacing = 25
        biasX = 1
        biasY = 7# 7 pretty good
        redFlag = [-3,-9]
        unStuck = [5,10]
        return hard_coords, width, height, spacing, biasX, biasY, redFlag, unStuck


# Coordinates of the game using googles built in minesweeper game


def startGame():
    global screenShot, x, y, click
    coords, width, height, spacing, biasX, biasY, redFlag, unStuck = setUpGame()

    pyautogui.moveTo(random.randrange(coords[0] + 100, coords[2] - 100),
                     random.randrange(coords[1] + 100,coords[3] - 100))
    pyautogui.click()
    time.sleep(2)
    screenShot = pyautogui.screenshot()

    while True:
        x = coords[0] + (spacing/2) + biasX
        y = coords[1] + (spacing/2) + biasY
        click = False
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
        if click == False:
            x = coords[0] + (spacing / 2) + biasX
            y = coords[1] + (spacing / 2) + biasY
            ifStuck(spacing, width, height, unStuck)





def doCalculations(spacing, redFlag):
    global screenShot, x, y
    # [(1),(2),(3),(4),....]
    possibleColors = [(25, 118, 210),(56, 142, 60),(211, 47, 47),(136, 51, 161),(255,143,0)]
    alternateColors = [(140, 57, 165),(156, 85, 159),(123, 31, 162),(161, 88, 161),
                       (134, 49, 161),(136, 51, 161)]
    # add up values of the incoming color and see if they are in a certain range
    # and then based on that number do stuff
    pixelColor = screenShot.getpixel((x, y))
    if pixelColor in possibleColors:
        flagNeighbors(possibleColors.index(pixelColor) + 1, spacing, redFlag)
        clickGreenBoxes(possibleColors.index(pixelColor) + 1, spacing, redFlag)
        return
    elif pixelColor in alternateColors:
        flagNeighbors(4, spacing, redFlag)
        clickGreenBoxes(4, spacing, redFlag)


def flagNeighbors(blockNumber, spacing, redFlag):
    global screenShot, x, y, click

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
            x, y, = origX, origY
            return
        if greenAmt > blockNumber and redAmt < blockNumber:
            x, y = origX, origY
            return

    rightClicks = 0
    clickLocations = []
    if (redAmt + greenAmt) <= blockNumber and redAmt != blockNumber:
        for pair in movePairs:
            x += pair[0]
            y += pair[1]
            pixelColor = screenShot.getpixel((x, y))
            if pixelColor in greenSquares:
                clickLocations.append([x,y])
                rightClicks += 1
            if rightClicks == greenAmt:
                break
    for location in clickLocations:
        pyautogui.moveTo(location[0],location[1])
        pyautogui.click(button='right')
        click = True
    time.sleep(.25)
    screenShot = pyautogui.screenshot()
    x, y, = origX, origY

    #Everything above here is for flagging neaighbors if they should be flagged

def clickGreenBoxes(blockNumber, spacing, redFlag):
    global screenShot, x, y, click
    origX, origY = x, y

    movePairs = [(-spacing, -spacing), (spacing, 0), (spacing, 0), (0, spacing), (0, spacing),
                 (-spacing, 0), (-spacing, 0), (0, -spacing), (spacing, 0)]
    greenSquares, redSquares = [(162, 209, 73),(170, 215, 81)], [(230,51,7),(242, 54, 7)]

    x += redFlag[0]
    y += redFlag[1]

    redNum = 0
    for pair in movePairs:
        x += pair[0]
        y += pair[1]
        pixelColor = screenShot.getpixel((x, y))
        if pixelColor in redSquares:
            redNum += 1

    x, y, = origX, origY

    if redNum == blockNumber:
        x += redFlag[0]
        y += redFlag[1]
        for pair in movePairs:
            x += pair[0]
            y += pair[1]
            pixelColor = screenShot.getpixel((x, y))
            if pixelColor in greenSquares:
                pyautogui.moveTo(x,y)
                pyautogui.click()
                click = True

    screenShot = pyautogui.screenshot()
    x, y, = origX, origY

def ifStuck(spacing, width, height, unStuck):
    global x, y, screenShot

    print("Trying to get unstuck")

    movePairs = [(-spacing, -spacing), (spacing, 0), (spacing, 0), (0, spacing), (0, spacing),
                 (-spacing, 0), (-spacing, 0), (0, -spacing), (spacing, 0)]
    greenSquares, redSquares = [(162, 209, 73), (170, 215, 81)], [(230, 51, 7), (242, 54, 7)]

    possibleColors = [(25, 118, 210), (56, 142, 60), (211, 47, 47), (136, 51, 161), (255, 143, 0)]
    alternateColors = [(140, 57, 165), (156, 85, 159), (123, 31, 162), (161, 88, 161),
                       (134, 49, 161), (136, 51, 161)]

    bestX, bestY = 0,0
    bestAverage = 100

    pixelColor = screenShot.getpixel((x,y))
    neighbors = 0
    neighborsTotal = 0
    for i in range(height):
        for j in range(width + 1):
            x -= unStuck[0]
            y -= unStuck[1]
            pixelColor = screenShot.getpixel((x, y))
            neighbors = 0
            neighborsTotal = 0
            if pixelColor in greenSquares:
                x += unStuck[0]
                y += unStuck[1]
                for pair in movePairs:
                    x += pair[0]
                    y += pair[1]
                    pixelColor = screenShot.getpixel((x, y))
                    if pixelColor in possibleColors:
                        neighbors += 1
                        neighborsTotal += possibleColors.index(pixelColor) + 1
                    elif pixelColor in alternateColors:
                        neighbors += 1
                        neighborsTotal += 4
            else:
                x += unStuck[0]
                y += unStuck[1]
            if (neighbors != 0 and neighborsTotal / neighbors < bestAverage):
                bestAverage = neighborsTotal / neighbors
                bestX, bestY = x, y
            x += spacing
        x += (-width - 1) * spacing
        y += spacing
    if bestY == 0 and bestX == 0:
        exit(0)
    pyautogui.click(bestX, bestY)
    pyautogui.moveTo(10,10)
    time.sleep(.25)
    screenShot = pyautogui.screenshot()
    time.sleep(.25)

startGame()