import pyautogui as py
import time
import os

from TTCC.GagTraining.constants import GagLevelLimit, MyGagLevel, MyGags, GagList, FRIENDS_BUTTON, SMILE_SYMBOL


def curDirPlus(filename):
    filestuff = os.path.join(r'GagTraining', os.path.join('images', filename))
    return os.path.join(os.getcwd(), filestuff)


def isHealthy():
    smile = py.locateOnScreen(curDirPlus(SMILE_SYMBOL), confidence=.9)
    if smile is not None:
        return True
    else:
        return False


def isGameOn():
    game = py.locateOnScreen(curDirPlus(FRIENDS_BUTTON), confidence=.9)
    if game is None:
        raise Exception("Game not found, is it on the main screen?")


def getGagInputs():
    for i in range(0, len(MyGags)):
        MyGags[i] = input("Enter amount of " + GagList[i] + " gags currently owned: ")
        MyGags[i] -= 1


def calculateGagLimits():
    for i in range(0, 8):
        if MyGagLevel[i] > 0:
            if MyGagLevel[i] == 1:
                GagLevelLimit[i] = [10]
            elif MyGagLevel[i] == 2:
                GagLevelLimit[i] = [10, 5]
            elif MyGagLevel[i] == 3:
                GagLevelLimit[i] = [15, 10, 5]
            elif MyGagLevel[i] == 4:
                GagLevelLimit[i] = [20, 15, 10, 5]
            elif MyGagLevel[i] == 5:
                GagLevelLimit[i] = [25, 20, 15, 10, 3]
            elif MyGagLevel[i] == 6:
                GagLevelLimit[i] = [25, 20, 15, 10, 7, 3]
            elif MyGagLevel[i] == 7:
                GagLevelLimit[i] = [30, 25, 20, 15, 7, 3]
            elif MyGagLevel[i] == 8:
                GagLevelLimit[i] = [30, 25, 20, 15, 7, 3, 1]
        else:
            GagLevelLimit[i] = [None]


def gameCountdown():
    # initial of the game
    py.FAILSAFE = True

    print("Starting", end="")
    for i in range(0, 5):
        print(".", end="")
        time.sleep(1)
    print("Go")
