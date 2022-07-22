import pyautogui as py
import time
import os
from PIL import Image
from pytesseract import pytesseract

from TTCC.GagTraining.constants import BATTLE_SYMBOL, GUIDE_BUTTON, TRUMPET_PLATE, WHISTLE_PLATE, BIKE_HORN_PLATE, \
    LOCK_IN_BUTTON, COG_BASE_PLATE
from TTCC.GagTraining.Helpers import curDirPlus


def getCogLevels():
    saveLocation = os.getcwd()+"/GagTraining/images/tmp/cog_plate.png"
    level_list = []
    while True:
        cogLevelPlates = py.locateAllOnScreen(curDirPlus(COG_BASE_PLATE), confidence=.8)
        if cogLevelPlates is not None:
            for plate in cogLevelPlates:
                py.screenshot(saveLocation, region=(plate.left, plate.top, plate.width+30, plate.height))
                level_list.append(getCogLevelFromImage(saveLocation))
            return level_list
        print("Cannot find cog level plates...")
        time.sleep(2)


def getCogLevelFromImage(image):
    path_to_tesseract = r'C:\Program Files\Tesseract-OCR\tesseract.exe'
    pytesseract.tesseract_cmd = path_to_tesseract
    img = Image.open(image)
    text = pytesseract.image_to_string(img)
    if "1" in text:
        return 1
    elif "2" in text:
        return 2
    elif "3" in text:
        return 3
    elif "4" in text:
        return 4
    elif "5" in text:
        return 5
    return 0


def check_gag(gag):
    gag_plate = py.locateOnScreen(curDirPlus(gag), confidence=.9)
    if gag_plate is not None:
        py.click(x=gag_plate.left, y=gag_plate.top)
        time.sleep(1)
    else:
        raise ValueError(f"NO {gag}")


def lock_in_gag():
    lock_in = py.locateOnScreen(curDirPlus(LOCK_IN_BUTTON), confidence=.9)
    if lock_in is not None:
        py.click(x=lock_in.left, y=lock_in.top)
    else:
        raise Exception("NO LOCK IN")


def chooseGag(max_level):
    try:
        if max_level == 1:
            gag_plate = BIKE_HORN_PLATE
        elif max_level == 2:
            gag_plate = BIKE_HORN_PLATE
        elif max_level == 3:
            gag_plate = WHISTLE_PLATE
        else:
            gag_plate = TRUMPET_PLATE
    except ValueError as e:
        print(e)
        gag_plate = TRUMPET_PLATE
    return gag_plate


def battle():
    battleOngoing = True
    while battleOngoing:
        if checkIfFighting():
            cog_levels = getCogLevels()
            max_level = max(cog_levels)
            try:
                gag_plate = chooseGag(max_level)
                check_gag(gag_plate)
            except ValueError:
                exception = True
                while exception:
                    print(f"No more level {max_level} gags, trying level {max_level - 1}...")
                    try:
                        max_level -= 1
                        gag_plate = chooseGag(max_level)
                        check_gag(gag_plate)
                        exception = False
                    except Exception:
                        pass
            try:
                lock_in_gag()
            except Exception:
                gag_plate = chooseGag(max_level-1)
                check_gag(gag_plate)
                lock_in_gag()
        if isBattleOver():
            battleOngoing = False


def checkIfFighting():
    symbolcoords = py.locateOnScreen(curDirPlus(BATTLE_SYMBOL), confidence=.9)
    if symbolcoords is not None:
        return True
    return False


def isBattleOver():
    guide = py.locateOnScreen(curDirPlus(GUIDE_BUTTON), confidence=.9)
    if guide is not None:
        return True
    return False
