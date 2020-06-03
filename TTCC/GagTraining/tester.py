import pyautogui as py, time, os


def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    fixMeLater = os.path.join('AdvancedScripts\Toontown',os.path.join('images', filename))
    return os.path.join(os.getcwd(), fixMeLater)

time.sleep(2)
region = py.locateOnScreen(imPath('Friends_Button.PNG'))
print(region)
