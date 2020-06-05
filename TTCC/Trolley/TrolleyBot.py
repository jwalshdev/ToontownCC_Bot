import pyautogui as py, time, os, cv2, winsound, tkinter as tk
root = tk.Tk()

"""TO DO:
-add folders respective to their games in images for better performance
"""

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
MEM_HIDDENCARD = 'Memory_Tile_'

MEM_CARDTOONUP = 'Toonup_Tile.PNG'
MEM_CARDTRAP = 'Trap_Tile.PNG'
MEM_CARDLURE = 'Dollar_Lure.PNG'
MEM_CARDSOUND = 'Sound_Tile.PNG'
MEM_CARDSQUIRT = 'Squirt_Tile.PNG'
MEM_CARDTHROW = 'Throw_Tile.PNG'
MEM_CARDDROP = 'Drop_Tile.PNG'

TUG_O_WAR = 'Tug_O_War.PNG'
TUG_O_WAR_GAMEOVER = 'Tug_O_War_Gameover.PNG'
TOW_POWER_METER = 'TOW_Power_Meter.PNG'
TOW_TOOFAST = 'TOW_TooFast.PNG'
TOW_TOOSLOW = 'TOW-TooSlow.PNG'
PLAY_LIST = [  MEMORY_GAME,]
playingGameTypeAgain=True   #this is for input on wanna play more minigames or no
amPlayingGame=False         #for the current state of playing (only for playingGame functions)

"""
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

def gameSelectionScreen():
    daGame, inList = checkGameInList()
    if inList is False:
        skipGame()
    else:
        startGame()
        playMe(daGame)  #the actual playing of the game
    waitForBeans()
    #game played now we should get our jellybeans and then wait until the gag menu shows up 


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
        func()


    print("Done playing, Did we win?")


def playMemoryGame():
    #For memory game
    #moving up down .35 seconds seems to be most accurate
    #moving left and right .27 looks right but might need to do a little slower, test further
    #could probably be .269, .268 etc and check to .26 and see further into there
    global amPlayingGame
    print("Playing Memory Game")
    DoneYet = False
    #getField()  #goes until it can find the game and start
    
    
    
    """In doing movement tests, comment the following code up to the set of three quotation marked comment"""
    bb = Board()
    bb.startSweepingCards()


    #MEM_HIDDENCARD
    #MEM_CARDTOONUP
    #MEM_CARDTRAP
    #MEM_CARDLURE
    #MEM_CARDSOUND ...
    #allHiddenCards 

    """end comment out"""
    DoneYet=True
    amPlayingGame=False



class Tyle(object):
    def __init__(self, cardType, tyleNum, alreadyMatched, isFacingUp):
        self.cardType = 'HIDDEN'    #types will be a string to their respective type
        self.tyleNum = tyleNum
        self.alreadyMatched = False
        self.isFacingUp = False
    
    def setCardType(self, newCardType):
        return newCardType.upper()
    
    def setMatched(self):
        self.alreadyMatched = True

    def setIsFacingUp(self, booleanVal):
        self.isFacingUp = booleanVal

    def notSameCard(self, otherTyleNum):
        if self.tyleNum != otherTyleNum:
            return True
        return False
        
    def checkMatch(self, otherCardType):
        return True if self.cardType != 'HIDDEN' and self.cardType == otherCardType else False
    
    def isTypeHidden(self):
        return True if self.cardType == 'HIDDEN' else False

smallList = [Tyle('HIDDEN',0, False,False),Tyle('HIDDEN',1,False,False),Tyle('HIDDEN',2,False,False),Tyle('HIDDEN',3,False,False),Tyle('HIDDEN',4,False,False),Tyle('HIDDEN',5,False,False),Tyle('HIDDEN',6,False,False),Tyle('HIDDEN',7,False,False)]
smallList2 = [Tyle('HIDDEN',8,False,False),Tyle('HIDDEN',9,False,False),Tyle('HIDDEN',10,False,False),Tyle('HIDDEN',11,False,False),Tyle('HIDDEN',12,False,False),Tyle('HIDDEN',13,False,False),Tyle('HIDDEN',14,False,False),Tyle('HIDDEN',15,False,False)]
smallList3 = [Tyle('HIDDEN',16,False,False),Tyle('HIDDEN',17,False,False),Tyle('HIDDEN',18,False,False),Tyle('HIDDEN',19,False,False),Tyle('HIDDEN',20,False,False),Tyle('HIDDEN',21,False,False),Tyle('HIDDEN',22,False,False),Tyle('HIDDEN',23,False,False)]
smallList4 = [Tyle('HIDDEN',24,False,False),Tyle('HIDDEN',25,False,False),Tyle('HIDDEN',26,False,False),Tyle('HIDDEN',27,False,False),Tyle('HIDDEN',28,False,False),Tyle('HIDDEN',29,False,False),Tyle('HIDDEN',30,False,False),Tyle('HIDDEN',31,False,False)]

def getHidTile(number):
    return MEM_HIDDENCARD + "%s" % number
    
Types = { 'TOONUP', 'TRAP','LURE','SOUND','SQUIRT','THROW','DROP'}
class Board():

    ToonupFound = []    #will be in format [(x1,y1),(x2,y2)] when full
    TrapFound = []      #and [(x1,y1)] or [] when not. These are the coords of both pairs
    LureFound = []
    SoundFound = []
    SquirtFound = []
    ThrowFound = []
    DropFound = []

    def __init__(self):
        super().__init__()  #idk 
        self.isPlaying = True
        self.board = [smallList,smallList2,smallList3,smallList4]
        self.x = 0
        self.y = 3
        self.playerLoc = (self.x,self.y)    #used to remember where original spot was (or is)

    def startSweepingCards(self):
        #start at bottom left corner
        #this will snake from bottom to up right one down right etc
        tempx=300
        for i in range(0,4):
            tempy = SCREEN_HEIGHT - (SCREEN_HEIGHT / 4)
            py.moveTo(tempx,tempy)
            MemMoveUp()
            #scan once moved off cell
            tempy-=195
            tempx+=35
            py.moveTo(tempx,tempy)
            MemMoveUp()
            #scanCardType(self.x, self.y)

            tempy-=195
            tempx+=35
            py.moveTo(tempx,tempy)

            MemMoveUp()
            
            tempy-=195
            tempx+=35
            py.moveTo(tempx,tempy)

            #x + 35 from front to back
            #y - 195 front to back
            #y start 815 every time (screenheight - 270)?
            MemMoveRight()
            tempx+=150
            py.moveTo(tempx,tempy)

            MemMoveDown()
            tempy+=195
            tempx-=35
            py.moveTo(tempx,tempy)

            MemMoveDown()
            tempy+=195
            tempx-=35
            py.moveTo(tempx,tempy)

            MemMoveDown()
            tempy+=195
            tempx-=35
            py.moveTo(tempx,tempy)

            if i < 3:
                MemMoveRight()
                tempx+=150
                py.moveTo(tempx,tempy)

        #maybe one last check of cards
        #if no more cards on table, return win
        #else return not a win, something went wrong
            
    def updatePlayerLoc(self):
        #for stamping (remembering) where the player location is to remember where to go back to so it can continue the snaking cycle
        self.playerLoc = (self.x, self.y)      

    def MemFlipCard(self):
        py.press('delete')

    def scanCardType(self, xPos, yPos):
        print('hi')

    def checkForMatches(self):
        #return 2 Tile tuples if there is, (0,0) if not
        for i in range(0,4):
            for j in range(0,8):    
                for a in range(0,4):
                    for b in range(0,8):
                        if not self.board[a][b].cardType == 'HIDDEN':
                            notSameTile = True if ((a,b) != (i,j)) else False
                            bothFacingUp = True if self.board[i][j].isFacingUp and self.board[a][b].isFacingUp else False
                            bothSameType = True if self.board[i][j].checkMatch(self.board[a][b]) else False
                            if notSameTile and bothFacingUp and bothSameType:
                                return ((i,j),(a,b))
        return (0,0)

    def moveUpCell(self):
        if self.y - 1 >= 0:
            MemMoveUp()
            self.y - 1
            
    def moveDownCell(self):
        if self.y + 1 <= 3:
            MemMoveDown()
            self.y + 1
            
    def moveRightCell(self):
        if self.x + 1 <= 7:
            MemMoveRight()
            self.x + 1
            
    def moveLeftCell(self):
        if self.x - 1 >= 0:
            MemMoveLeft()
            self.x - 1

    

def MemMoveLeft():
    moveBy('a',.267)

def MemMoveRight():
    moveBy('d',.267)

def MemMoveUp():
    moveBy('w',.35)

def MemMoveDown():
    moveBy('s',.35)


def curDirMem(filename):
    filestuff = os.path.join('AdvancedScripts\\TTCC\\Trolley', os.path.join(r'images\MemGame', filename))        #this part is for me, as my current working directory is further back (will change when I change cwd)
    return os.path.join(os.getcwd(),filestuff)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#this part has to be redone in c++ because python is too slow for this, pull the .lib file from there and put it here
def playTugOWarGame():
    #global amplayingAgain
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
    
    """if(py.locateOnScreen(curDirPlus(TOW_POWER_METER), confidence=.9)) is None:
        amPlayingGame=False
        raise Exception("Could not find Tug of War, Exiting Function")
        return'"""

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

    #amPlayingGame=False

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


def waitForBeans():
    dabeans = py.locateOnScreen(curDirPlus(GETTING_BEANS),confidence=.9)
    while dabeans is None:
        time.sleep(1)
        dabeans = py.locateOnScreen(curDirPlus(GETTING_BEANS),confidence=.9)

def afterGame():
    """Loops indefinitly as playingGameTypeAgain is True"""
    global playingGameTypeAgain
    #first wait until it is on jellybean page
    beans = py.locateOnScreen(curDirPlus(GETTING_BEANS))
    while beans is None:
        time.sleep(.5)
        beans = py.locateOnScreen(curDirPlus(GETTING_BEANS))

    playingGameTypeAgain = wannaPlayAgain()
    while playingGameTypeAgain is True:
        playingGameTypeAgain = wannaPlayAgain()
        if playingGameTypeAgain:
            time.sleep(.5)
            playAgain() #click play again
            time.sleep(3)   #might have to increase for slower computers (could decrease for faster)
            gameSelectionScreen()
        time.sleep(2)
    time.sleep(2)  

def curDirPlus(filename):
    filestuff = os.path.join('AdvancedScripts\\TTCC\\Trolley', os.path.join('images', filename))        #this part is for me, as my current working directory is further back (will change when I change cwd)
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
        word = curDirPlus(PLAY_LIST[i])
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
