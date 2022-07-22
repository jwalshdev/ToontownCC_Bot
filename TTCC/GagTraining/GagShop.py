import pyautogui as py
import time

from TTCC.GagTraining.constants import TRUMPET_PLATE, WHISTLE_PLATE, BIKE_HORN_PLATE, TU_START_GAG, MyGagLevel, MyGags, \
    GagLevelLimit, GAG_MENU_EXIT_BUTTON, GAG_MENU
from TTCC.GagTraining.Movement import moveBy, turnAround
from TTCC.GagTraining.Helpers import curDirPlus


def buyByType(type):
    if type == "sound":
        trumpet = py.locateOnScreen(curDirPlus(TRUMPET_PLATE), confidence=.85)
        if trumpet:
            print("Buying trumpet")
            for i in range(5):
                py.click(trumpet)
                time.sleep(.1)
        whistle = py.locateOnScreen(curDirPlus(WHISTLE_PLATE), confidence=.85)
        if whistle:
            print("Buying whistle")
            for i in range(10):
                py.click(whistle)
                time.sleep(.1)
        bike_horn = py.locateOnScreen(curDirPlus(BIKE_HORN_PLATE), confidence=.85)
        if bike_horn:
            print("Buying bike horn")
            for i in range(15):
                py.click(bike_horn)
                time.sleep(.1)
    exit_store()


def buyAllGagsNeeded():
    startLoc = py.locateOnScreen(curDirPlus(TU_START_GAG), confidence=.8)
    if startLoc is None:
        resetTalkingToClerk()
        return
    y = startLoc[1] + 20
    dx, dy = 80, 50

    for i in range(0, 8):
        x = startLoc[0] + 150
        if MyGagLevel[i] > 0:
            x += (dx * (MyGagLevel[i] - 1))
            thisgagtrack = MyGags[i]
            amountAtEnd = thisgagtrack[-1]

            while amountAtEnd < GagLevelLimit[i][-1]:
                py.click(x, y)
                time.sleep(.1)
                amountAtEnd += 1
        y += dy
        exit_store()


def exit_store():
    exitStore = py.locateOnScreen(curDirPlus(GAG_MENU_EXIT_BUTTON), confidence=.9)
    if exitStore is None:
        return
    py.moveTo(exitStore)
    py.click()
    time.sleep(1)
    moveBy('s', .3)


def leaveGagClerk():
    turnAround()
    moveBy('w', 4)


def swipeGags():
    startLoc = py.locateOnScreen(curDirPlus(TU_START_GAG))
    if startLoc is None:
        resetTalkingToClerk()
        return
    x = startLoc[0] + 150
    y = startLoc[
            1] + 20
    dx, dy = 80, 50

    for i in range(0, 8):
        for j in range(0, 8):
            py.moveTo(x, y, duration=.2)
            x += dx
        x = startLoc[0] + 150
        y += dy


def walkToGagClerk():
    moveBy('d', .15)
    moveBy('w', 2)
    while True:
        if py.locateOnScreen(curDirPlus(GAG_MENU), confidence=.9) is not None:
            return
        print("Cannot find gag menu...")
        time.sleep(1)
        resetTalkingToClerk()


def resetTalkingToClerk():
    moveBy('s', 1)
    time.sleep(.1)
    moveBy('w', 1)


def CheckIfTrading():
    menucoords = py.locateOnScreen(curDirPlus(GAG_MENU))
    if menucoords is not None:
        return True
    return False