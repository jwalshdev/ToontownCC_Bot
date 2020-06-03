import pyautogui as py, time, os
TUG_O_WAR = 'Tug_O_War.PNG'
HOWDY = 'Friends_Button.PNG'
TUG_O_WAR_GAMEOVER = 'Tug_O_War_Gameover.PNG'
ONLINEFRIENDS = 'OnlineToonFriends.PNG'
ENOUGHGAGS = 'IHaveEnoughGags.PNG'
WAVE = 'Wave.PNG'

PLAY_LIST = [ HOWDY ,]


def main():
    time.sleep(2)
    thing = py.locateOnScreen(curDirPlus(HOWDY))
    print(thing)
    amIDone = False
    tappertime=0.0
    while not amIDone:
        amt = incOrDecBy()
        tappertime = tappertime + amt
        if tappertime < 0:
            tappertime = 0
        print(tappertime)
        strafe(tappertime)
        amIDone = TOW_isGameOver()
    print("yay")

def incOrDecBy():
    amount = 0.0
    extremeAmt = .015
    normalAmt = .0005
    #I feel there is a better way than how I am doing it,
    #but I will first check for too slow or too fast and return relative to that
    bigspeed = py.locateOnScreen(curDirPlus(WAVE),confidence=.9)
    if bigspeed is not None:
        print("Slowing down with ")
        amount = extremeAmt        #increase the time
        return amount
    bigspeed = py.locateOnScreen(curDirPlus(ENOUGHGAGS),confidence=.9)
    if bigspeed is not None:
        print("Speeding Up with ")
        amount = 0-extremeAmt       #decrease the time
        return amount
    print("None of that shit")
    return -normalAmt

def strafe(sleep_interval):
    print("Strafe")
    if sleep_interval < 0:
        sleep_interval = .1
    moveTime = .1
    moveBy('a',moveTime)
    time.sleep(sleep_interval)
    moveBy('d',moveTime)


def TOW_isGameOver():
    amIFound = py.locateOnScreen(curDirPlus(ONLINEFRIENDS))
    if amIFound is None:
        return False
    return True

def moveBy(key, amount):
    py.keyDown(key)
    time.sleep(amount)
    py.keyUp(key)

def wait_until(somepredicate, timeout, period=0.25, *args, **kwargs):
  mustend = time.time() + timeout
  while time.time() < mustend:
    if somepredicate(*args, **kwargs): return True
    time.sleep(period)
  return False

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    fixMeLater = os.path.join('AdvancedScripts\\TTCC\\Trolley',os.path.join('images', filename))
    return os.path.join(os.getcwd(), fixMeLater)

def curDirPlus(filename):
    filestuff = os.path.join('AdvancedScripts\\TTCC\\Trolley', imPath(filename))        #this part is for me, as my current working directory is further back (will change when I change cwd)
    return os.path.join(os.getcwd(),filestuff)

if __name__ == "__main__":
    main()