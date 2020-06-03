import pyautogui as py, time, os, cv2, winsound, tkinter as tk
root = tk.Tk()

SCREEN_WIDTH = root.winfo_screenwidth()
SCREEN_HEIGHT = root.winfo_screenheight()
TROLLEY = 'Trolley.PNG'
PLAY_BUTTON = 'Play_Button.PNG'
PLAY_AGAIN_BUTTON = 'Play_Again.PNG'
SKIP_BUTTON = 'Skip_Button.PNG'
PLAYGROUND_BUTTON = 'Exit_To_Playground_Button.PNG'
GETTING_BEANS = 'GettingJellyBeans.PNG'

FREIND = 'Friends_Button.PNG'
MEMORY_GAME = 'Memory_Game.PNG'
TUG_O_WAR = 'Tug_O_War.PNG'
TUG_O_WAR_GAMEOVER = 'Tug_O_War_Gameover.PNG'
TOW_POWER_METER = 'TOW_Power_Meter.PNG'
TOW_TOOFAST = 'TOW_TooFast.PNG'
TOW_TOOSLOW = 'TOW-TooSlow.PNG'
PLAY_LIST = [  MEMORY_GAME,]
playingAgain=True
amPlayingGame=False

"""
(yes I used a 0, using a O is a keyword)
THINGS TO N0TE:
1) When you hear beeps, that means it is searching for yes or no, yes is right half of screen and no is left 
"""
def main():
    global TUG_O_WAR
    setUpPreReq()
    time.sleep(2)

    #I know these are good, so to move along after I will start from gag shop menu
    moveOntoTrolley()
    checkIfOnTrolley()
    #uncomment these when ready

    #playAgain()


    #now that we are on trolley, check if the following game is in known game list
    #if it is not, skip and play again

    gameSelectionScreen()
    afterGame()
    exitToPlayground()


def playMe(daGame):
    global amPlayingGame
    amPlayingGame = True
    while amPlayingGame:
         #while amPlaying, keep looping around to play the game, once game is won we will set this to false to exit loop
        gameSolutions = {
            'Tug_O_War.PNG': playTugOWarGame,
            'Memory_Game.PNG': playMemoryGame
        }
        # Get the function from switcher dictionary
        func = gameSolutions.get(daGame, lambda: "Invalid Game")
        # Execute the function
        func(amPlayingGame)


    print("Done playing, Did we win?")


def playMemoryGame(amPlayingGame):
    global playingAgain
    print("Playing Memory Game")
    DoneYet = False
    #getField()  #goes until it can find the game and start
    
    #lets calculate how much time to walk up
    moveBy('w',1.3)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#this part has to be redone in c++ because python is too slow for this, pull the .lib file from there and put it here
def playTugOWarGame(amPlayingGame):
    global playingAgain
    print("Playing Tug of War Game")
    DoneYet = False
    xOffset = (SCREEN_WIDTH / 10)
    #so the offset is the space shortened amount on both sides 
    #the Y is calculated by getting the bottom fifth of the screen and starting at the first point of it
    #width is subtracting 2 times the offset
    #height is the point measured before taken away from the screen height
    GameOverRegion = (xOffset,(SCREEN_HEIGHT - (SCREEN_HEIGHT / 5)), SCREEN_WIDTH - (2 * xOffset), SCREEN_HEIGHT - (SCREEN_HEIGHT - (SCREEN_HEIGHT / 5)))

    w = (SCREEN_WIDTH)/2
    h = SCREEN_HEIGHT
    
    GameRegion = (w-(w/6),h-(h-(h/10)), 320, 400)
    time.sleep(2) #wait a bit and then try to find the power meter 
    
    if(py.locateOnScreen(curDirPlus(TOW_POWER_METER), confidence=.9)) is None:
        raise Exception("Could not find Tug of War, Exiting Function")
        playingAgain=False
        return

    print("Time to Play some Tug o War")
    tappertime = .5
    TOW_Tug(tappertime) #first we will bring out bar up a bit
    while not DoneYet:
        #now we are playing the game, we have our game region
        #inputs are 'a' and 'd' to tap left and right, the difference between taps must be done by certain intervals
        #we will have a function that does intervals of left - sleep - right - sleep and take in for amount to sleep
        #left and right can be done quickly
        #
        #we will have a variable that will be a placeholder for the sleep_interval in between taps
        #This variable, tappertime, will start at .5 and increments and decrements will start at .15 (if not too slow or too fast) and .05 if too slow or too fast found
        #a function incOrDecBy() will return a negative or positive float to be added into the tappertime
        #
        #
        amt = incOrDecBy(GameRegion=GameRegion)
        tappertime += amt
        TOW_Tug(tappertime)
        DoneYet = TOW_isGameOver(GameOverRegion)

    amPlayingGame=False

def incOrDecBy(GameRegion):
    amount = 0.0
    extremeAmt = .05
    normalAmt = .15
    #I feel there is a better way than how I am doing it,
    #but I will first check for too slow or too fast and return relative to that
    bigspeed = py.locateOnScreen(curDirPlus(TOW_TOOFAST),GameRegion,confidence=.9)
    if bigspeed is not None:
        amount = extremeAmt        #increase the time
        return amount
    bigspeed = py.locateOnScreen(curDirPlus(TOW_TOOSLOW),GameRegion,confidence=.9)
    if bigspeed is not None:
        amount = 0-extremeAmt       #decrease the time
        return amount

    return 0-normalAmt


def TOW_Tug(sleep_interval):
    moveTime = .2
    moveBy('a',moveTime)
    time.sleep(sleep_interval)
    moveBy('d',moveTime)
    time.sleep(sleep_interval)


def TOW_isGameOver(gameOverRegion):
    amIFound = py.locateOnScreen(curDirPlus(TUG_O_WAR_GAMEOVER),gameOverRegion)
    if amIFound is None:
        return False
    return True

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#Everything below this line is the process of looping around to navigate the screen to play games if found in list of games known to play
#add game play above this section as this section will be last
def gameSelectionScreen():
    daGame, inList = checkGameInList()
    if inList is False:
        skipGame()
    else:
        startGame()
        playMe(daGame)  #the actual playing of the game
 
        #game played now we should get our jellybeans and wait until the gag menu shows up
    #game skipped/finished and gag menu pulled up
    time.sleep(1.5)
    

def afterGame():
    """Loops indefinitly as playingAgain is True"""
    global playingAgain
    #first wait until it is on jellybean page
    beans = py.locateOnScreen(curDirPlus(GETTING_BEANS))
    while beans is None:
        time.sleep(.5)
        beans = py.locateOnScreen(curDirPlus(GETTING_BEANS))

    playingAgain = wannaPlayAgain()
    while playingAgain is True:
        playingAgain = wannaPlayAgain()
        if playingAgain:
            time.sleep(.5)
            playAgain() #click play again
            time.sleep(3)   #might have to increase for slower computers (could decrease for faster)
            gameSelectionScreen()
        time.sleep(2)
    time.sleep(2)  

def imPath(filename):
    """A shortcut for joining the 'images/'' file path, since it is used so often. Returns the filename with 'images/' prepended."""
    fixMeLater = os.path.join('AdvancedScripts\\TTCC\\Trolley',os.path.join('images', filename))
    return os.path.join(os.getcwd(), fixMeLater)

def curDirPlus(filename):
    filestuff = os.path.join('AdvancedScripts\\TTCC\\Trolley', imPath(filename))        #this part is for me, as my current working directory is further back (will change when I change cwd)
    return os.path.join(os.getcwd(),filestuff)

def checkGameInList():
    #3 ways to handle this that I can think of
        # 1) run through all play_list pics looking for pic located on screen
        # 2) screen_shot the area and compare this area to list
        # 3) Screen_shot, recognize string and compare by that
        # If improving later, this could be done in C++ and called through python
    isItIn = False
    Game = ""
    for i in range(0,len(PLAY_LIST)):
        word = imPath(PLAY_LIST[i])
        cc = py.locateOnScreen(curDirPlus(word))
        #print(cc)
        if cc is not None:
            print(cc)
            Game = PLAY_LIST[i]
            isItIn = True
    return Game, isItIn


def wannaPlayAgain():
    countdownSounds()
    """For this, play again will be determined by mouse, if it's on the right side (not half but generally right) then not playing again """
    #we'll make it the right half of the screen (y value could be anything)
    passMe = SCREEN_WIDTH * (1.0/2)
    myX, myY = py.position()
    if myX >= passMe:
        return True
    return False

def playAgain():
    print("Clicking Play Again")
    cc = py.locateOnScreen(curDirPlus(PLAY_AGAIN_BUTTON))
    py.moveTo(cc)
    py.click()
    time.sleep(.4)

def exitToPlayground():
    print("Exiting to Playground")
    cc = py.locateOnScreen(curDirPlus(PLAYGROUND_BUTTON))
    py.moveTo(cc)
    py.click()
    time.sleep(.5)

def startGame():
    print("Clicking Play Button")
    cc = py.locateOnScreen(curDirPlus(PLAY_BUTTON))
    py.moveTo(cc)
    py.click()
    time.sleep(.285)

def countdownSounds():
    frequency = 500  
    duration = 500
    for i in range(0,3):
        winsound.Beep(frequency,duration)
        time.sleep(.5)
    frequency=1000
    duration=600
    winsound.Beep(frequency,duration)
    time.sleep(1)

def skipGame():
    print("Skipping Game")
    cc = py.locateOnScreen(curDirPlus(SKIP_BUTTON))
    py.moveTo(cc)
    py.click()
    time.sleep(1.4)


def checkIfOnTrolley():

    winsound.Beep(100,300)
    findMe = py.locateOnScreen(curDirPlus(TROLLEY),confidence=.9)
    if findMe is None:
        raise Exception("No Trolley Found")
        return
    print("On Trolley, hopefully no one else is on")
    time.sleep(12)
    
    
def moveOntoTrolley():
    moveBy('w',2)
    time.sleep(4)
    winsound.Beep(100,300)

def moveBy(key, amount):
    py.keyDown(key)
    time.sleep(amount)
    py.keyUp(key)


def setUpPreReq():
    global TUG_O_WAR,MEMORY_GAME,PLAYGROUND_BUTTON,SKIP_BUTTON,PLAY_AGAIN_BUTTON,PLAY_BUTTON,TROLLEY
    py.FAILSAFE=True

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||

if __name__ == "__main__":
    main()