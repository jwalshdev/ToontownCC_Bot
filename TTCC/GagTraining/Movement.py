import pyautogui as py
import time


def moveBy(key, amount):
    py.keyDown(key)
    time.sleep(amount)
    py.keyUp(key)


def turnBy(angle, dir):
    if dir.upper()[0] == "R":
        key = 'd'
    else:
        key = 'a'
    if angle == 90:
        moveBy(key, .775)
    elif angle == 180:
        moveBy(key, 1.7)
    elif angle == 45:
        moveBy(key, .35)
    else:
        raise Exception("Invalid turn angle!")


def turnAround():
    turnBy(180, "R")


def fromGagToSeaweedStreet():
    moveBy('w', .3)
    moveBy('a', .8)
    moveBy('w', 2)
    moveBy('a', .8)
    moveBy('w', 1)


def toGagFromSeaweedStreet():
    moveBy('w', .25)
    turnBy(90, "R")
    moveBy('w', 2)
    turnBy(90, "R")
    moveBy('w', 1)


def toBattleSpot():
    moveBy('w', .6)
    turnBy(90, "L")
    moveBy('w', .6)


def fromBattleSpot():
    turnBy(45, "L")
    moveBy('w', 3)
