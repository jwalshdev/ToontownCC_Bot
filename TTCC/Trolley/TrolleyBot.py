import pyautogui as py, time, os, cv2, winsound, tkinter as tk
from threading import Thread
from pynput.mouse import Button, Controller
from pynput.keyboard import Listener, KeyCode, Key, Controller

root = tk.Tk()
keyboard = Controller()
mouse = Controller()

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

""" 'KNOWN' GAME LIST"""
MEMORY_GAME = 'Memory_Game.PNG'
RING_GAME = 'RingGame.PNG' 
TUG_O_WAR = 'Tug_O_War.PNG'
"""\END 'KNOWN' GAME LIST"""

MEM_HIDDENCARD = 'Memory_Tile_'

MEM_CARDTOONUP = 'Toonup_Tile.PNG'
MEM_CARDTRAP = 'Trap_Tile.PNG'
MEM_CARDLURE = 'Dollar_Lure.PNG'
MEM_CARDSOUND = 'Sound_Tile.PNG'
MEM_CARDSQUIRT = 'Squirt_Tile.PNG'
MEM_CARDTHROW = 'Throw_Tile.PNG'
MEM_CARDDROP = 'Drop_Tile.PNG'


TUG_O_WAR_GAMEOVER = 'Tug_O_War_Gameover.PNG'
TOW_POWER_METER = 'TOW_Power_Meter.PNG'
TOW_TOOFAST = 'TOW_TooFast.PNG'
TOW_TOOSLOW = 'TOW_TooSlow.PNG'
TOW_isRunning = False
TOW_GameOvertimer = None

ToonupFound = []    #will be in format [(x1,y1),(x2,y2)] when considered ready to work with
TrapFound = []      #and [(x1,y1)] or [] when not. These are the coords of both pairs
LureFound = []
SoundFound = []
SquirtFound = []
ThrowFound = []
DropFound = []
NoneFound = []
CurrFlippedUp = []      #this is for keeping track of which is flipped open or not
                        #when this reaches 2, the next flip will erase this and put the new tile as the first
PLAY_LIST = [  MEMORY_GAME, ]
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
            'Memory_Game.PNG': playMemoryGame,
            'RingGame.PNG': playRingGame
        }
        # Get the function from switcher dictionary
        func = gameSolutions.get(daGame, lambda: "Invalid Game")
        # Execute the function
        func()


    print("Done playing, Did we win?")

def playRingGame():
    getRingType()   #gets the ring in bottom right corner and uses that to find other of that type 



#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
"""TASK:
-Eventually move mouse to right side in green wall so its not in the way and it can replay again
-Keep track of amt of cards flipped up 
-also account for the matches in the snake loop

"""

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
    """
    for j in range(0,4):
        for i in range(0,8):
            bb.scanCertainCard(i,j)
    """
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
    if number > 31:
        number = 31
    return MEM_HIDDENCARD + "%s" % number + ".PNG"
    
Types = { 'TOONUP', 'TRAP','LURE','SOUND','SQUIRT','THROW','DROP'}
class Board():
    def __init__(self):
        super().__init__()  #idk 
        self.isPlaying = True
        self.board = [smallList,smallList2,smallList3,smallList4]
        self.x = 0
        self.y = 3
        self.playerLoc = (self.x,self.y)    #used to remember where original spot was (or is)
    def clickMoveUpAndScan(self):
        self.MemFlipCard()
        time.sleep(.05)
        self.moveUpCell()
        self.scanCertainCard(self.x, self.y+1)
        ogX = self.x
        ogY = self.y
        res = self.checkMatch()
        if(res is not None):
            firstLoc = res[0]
            secondLoc = res[1]

            #once they are flipped, go back to the original spot
            #self.scanCertainCard(self.x, self.y+1)
    def clickMoveRightAndScan(self):
        self.MemFlipCard()
        time.sleep(.05)
        self.moveRightCell()
        self.scanCertainCard(self.x-1, self.y)
        res = self.checkMatch()
        if(res is not None):
            firstLoc = res[0]
            secondLoc = res[1]

        return
    def clickMoveDownAndScan(self):
        self.MemFlipCard()
        time.sleep(.05)
        self.moveDownCell()
        self.scanCertainCard(self.x, self.y-1)
        res = self.checkMatch()
        if(res is not None):
            firstLoc = res[0]
            secondLoc = res[1]
        #else if is none, match was found and made already

        return
    
    def startSweepingCards(self):
        #start at bottom left corner
        #this will snake from bottom to up right one down right etc
        #tempx=300
        sleep_time = .05
        for i in range(0,4):
 
            self.clickMoveUpAndScan()
            self.clickMoveUpAndScan()
            self.clickMoveUpAndScan()
            self.clickMoveRightAndScan()
            self.clickMoveDownAndScan()
            self.clickMoveDownAndScan()
            self.clickMoveDownAndScan()
            if i < 3:
                self.clickMoveRightAndScan()
            else:
                tempX = self.x
                tempY = self.y
                self.MemFlipCard()
                self.moveUpCell()
                self.scanCertainCard(tempX, tempY)

        print(ToonupFound)
        print(TrapFound)
        print(LureFound)
        print(SoundFound)
        print(SquirtFound)
        print(ThrowFound)
        print(DropFound)
        print(NoneFound)
        #maybe one last check of cards
        #if no more cards on table, return win
        #else return not a win, something went wrong
            
    def checkMatch(self):
        #will return the list if match, else none
        if(len(ToonupFound) >= 2):
            return ToonupFound
        elif(len(TrapFound)>=2):
            return TrapFound
        elif(len(LureFound) >=2):
            return LureFound
        elif(len(SoundFound) >=2):
            return SoundFound
        elif(len(SquirtFound) >=2):
            return SquirtFound
        elif(len(ThrowFound) >=2):
            return ThrowFound
        elif(len(DropFound) >=2):
            return DropFound
        else:
            return None
    def scanCertainCard(self,locX,locY):
        global ToonupFound, TrapFound, LureFound, SoundFound, SquirtFound, ThrowFound, DropFound, NoneFound
        #scans the (locX,locY) tile to see which it is and adds that to array of types
        #returns type
        #this will be redone in cpython
        tileNum = (8 * locY) + locX
        if(locY == 0): #if in first row
            daX = SCREEN_WIDTH/5 
            daY = SCREEN_HEIGHT/4.5 
            rwidth = 140 
            rheight = 130
            daRegion = (int(daX), int(daY), rwidth, rheight)
            daX += (locX * rwidth)
            if(py.locateOnScreen(curDirMem(getHidTile(tileNum)),region=daRegion, confidence=.5) != None):
                print("Hidden Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTOONUP),region=daRegion, confidence=.15) != None):
                ToonupFound.append((locX,locY))
                print("Toonup Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTRAP),region=daRegion, confidence=.15) != None):
                TrapFound.append((locX,locY))
                print("Trap Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDLURE),region=daRegion, confidence=.15) != None):
                LureFound.append((locX,locY))
                print("Lure Found at: ",locX,locY)
            
            elif(py.locateOnScreen(curDirMem(MEM_CARDSOUND),region=daRegion, confidence=.15) != None):
                SoundFound.append((locX,locY))
                print("Sound Found at: ",locX,locY)

            elif(py.locateOnScreen(curDirMem(MEM_CARDSQUIRT),region=daRegion, confidence=.15) != None):
                SquirtFound.append((locX,locY))
                print("Squirt Found at: ",locX,locY)

            elif(py.locateOnScreen(curDirMem(MEM_CARDTHROW),region=daRegion, confidence=.15) != None):
                ThrowFound.append((locX,locY))
                print("Throw Found at: ",locX,locY)

            elif(py.locateOnScreen(curDirMem(MEM_CARDDROP),region=daRegion, confidence=.15) != None):
                DropFound.append((locX,locY))
                print("Drop Found at: ",locX,locY)
            else:
                NoneFound.append((locX,locY))
                print("No Tile Found at: ",locX,locY)
        elif (locY == 1):
            rwidth = 150 
            rheight = 130
            daX = SCREEN_WIDTH/5 - 35 + (locX * rwidth)
            daY = SCREEN_HEIGHT/4.5 + rheight + 30
            daRegion = (int(daX), int(daY), rwidth, rheight)
            if(py.locateOnScreen(curDirMem(getHidTile(tileNum)),region=daRegion, confidence=.22) != None):
                print("Hidden Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTOONUP),region=daRegion, confidence=.15) != None):
                ToonupFound.append((locX,locY))
                print("Toonup Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTRAP),region=daRegion, confidence=.15) != None):
                TrapFound.append((locX,locY))
                print("Trap Found at: ",locX,locY) 
            elif(py.locateOnScreen(curDirMem(MEM_CARDLURE),region=daRegion, confidence=.15) != None):
                LureFound.append((locX,locY))
                print("Lure Found at: ",locX,locY)          
            elif(py.locateOnScreen(curDirMem(MEM_CARDSOUND),region=daRegion, confidence=.15) != None):
                SoundFound.append((locX,locY))
                print("Sound Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDSQUIRT),region=daRegion, confidence=.15) != None):
                SquirtFound.append((locX,locY))
                print("Squirt Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTHROW),region=daRegion, confidence=.15) != None):
                ThrowFound.append((locX,locY))
                print("Throw Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDDROP),region=daRegion, confidence=.15) != None):
                DropFound.append((locX,locY))
                print("Drop Found at: ",locX,locY)
            else:
                NoneFound.append((locX,locY))
                print("No Tile Found at: ",locX,locY)
        elif(locY == 2):      
            rwidth = 155 
            rheight = 130
            daX = SCREEN_WIDTH/5 - (35) + (locX * rwidth)
            daY = SCREEN_HEIGHT/4.5 + (2 * rheight) + (33 * 2)
            daRegion = (int(daX), int(daY), rwidth, rheight)
            if(py.locateOnScreen(curDirMem(getHidTile(tileNum)),region=daRegion, confidence=.32) != None):
                print("Hidden Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTOONUP),region=daRegion, confidence=.15) != None):
                ToonupFound.append((locX,locY))
                print("Toonup Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTRAP),region=daRegion, confidence=.15) != None):
                TrapFound.append((locX,locY))
                print("Trap Found at: ",locX,locY) 
            elif(py.locateOnScreen(curDirMem(MEM_CARDLURE),region=daRegion, confidence=.15) != None):
                LureFound.append((locX,locY))
                print("Lure Found at: ",locX,locY)          
            elif(py.locateOnScreen(curDirMem(MEM_CARDSOUND),region=daRegion, confidence=.15) != None):
                SoundFound.append((locX,locY))
                print("Sound Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDSQUIRT),region=daRegion, confidence=.15) != None):
                SquirtFound.append((locX,locY))
                print("Squirt Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTHROW),region=daRegion, confidence=.15) != None):
                ThrowFound.append((locX,locY))
                print("Throw Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDDROP),region=daRegion, confidence=.15) != None):
                DropFound.append((locX,locY))
                print("Drop Found at: ",locX,locY)
            else:
                NoneFound.append((locX,locY))
                print("No Tile Found at: ",locX,locY)
        else:
            rwidth = 167 
            rheight = 130
            daX = SCREEN_WIDTH/5 - (30 * 3) + locX * rwidth
            daY = (SCREEN_HEIGHT/4.5) + (3 * rheight) + 110
            daRegion = (int(daX), int(daY), rwidth, rheight)
            py.moveTo(daX,daY)
            if(py.locateOnScreen(curDirMem(getHidTile(tileNum)),region=daRegion, confidence=.16) != None):
                print("Hidden Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTOONUP),region=daRegion, confidence=.15) != None):
                ToonupFound.append((locX,locY))
                print("Toonup Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTRAP),region=daRegion, confidence=.15) != None):
                TrapFound.append((locX,locY))
                print("Trap Found at: ",locX,locY) 
            elif(py.locateOnScreen(curDirMem(MEM_CARDLURE),region=daRegion, confidence=.15) != None):
                LureFound.append((locX,locY))
                print("Lure Found at: ",locX,locY)          
            elif(py.locateOnScreen(curDirMem(MEM_CARDSOUND),region=daRegion, confidence=.15) != None):
                SoundFound.append((locX,locY))
                print("Sound Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDSQUIRT),region=daRegion, confidence=.15) != None):
                SquirtFound.append((locX,locY))
                print("Squirt Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDTHROW),region=daRegion, confidence=.15) != None):
                ThrowFound.append((locX,locY))
                print("Throw Found at: ",locX,locY)
            elif(py.locateOnScreen(curDirMem(MEM_CARDDROP),region=daRegion, confidence=.15) != None):
                DropFound.append((locX,locY))
                print("Drop Found at: ",locX,locY)
            else:
                NoneFound.append((locX,locY))
                print("No Tile Found at: ",locX,locY)
    def updatePlayerLoc(self):
        #for stamping (remembering) where the player location is to remember where to go back to so it can continue the snaking cycle
        self.playerLoc = (self.x, self.y)      
    def MemFlipCard(self):
        py.press('delete')
        if(len(CurrFlippedUp) >= 2):    #if 2 (or somehow more) cards are hs
            CurrFlippedUp.clear()
            CurrFlippedUp.append((self.x,self.y))
        else:
            CurrFlippedUp.append((self.x,self.y))
    def moveUpCell(self):
        if self.y - 1 >= 0:
            MemMoveUp()
            self.y -= 1      
    def moveDownCell(self):
        if self.y + 1 <= 3:
            MemMoveDown()
            self.y += 1      
    def moveRightCell(self):
        if self.x + 1 <= 7:
            MemMoveRight()
            self.x += 1     
    def moveLeftCell(self):
        if self.x - 1 >= 0:
            MemMoveLeft()
            self.x -= 1


def MemMoveLeft():
    moveBy('a',.265)
def MemMoveRight():
    moveBy('d',.265)
def MemMoveUp():
    moveBy('w',.35)
def MemMoveDown():
    moveBy('s',.35)



#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
"""Works for the most part, all tests are either ties or wins, could improve more"""

def playTugOWarGame():
    global TOW_isRunning
    global amPlayingGame
    print("Playing Tug of War Game")
    DoneYet = False
    #xOffset = (SCREEN_WIDTH / 10)
    #so the offset is the space shortened amount on both sides 
    #the Y is calculated by getting the bottom fifth of the screen and starting at the first point of it
    #width is subtracting 2 times the offset
    #height is the point measured before taken away from the screen height
    #GameOverRegion = (xOffset,(SCREEN_HEIGHT - (SCREEN_HEIGHT / 5)), SCREEN_WIDTH - (2 * xOffset), SCREEN_HEIGHT - (SCREEN_HEIGHT - (SCREEN_HEIGHT / 5)))

    #w = (SCREEN_WIDTH)/2
    #h = SCREEN_HEIGHT
    
    #GameRegion = (int(w-(w/6)),int(h-(h-(h/10))), 320, 400)
    time.sleep(1.5) #wait a bit and then try to find the power meter 

    print("Time to Play some Tug o War")
    #tappertime = .5
    #TOW_Tug(tappertime) #first we will bring out bar up a bit
    #amt = incOrDecBy(GameRegion)
    TOW_isRunning=True
    t1 = ThreadWithReturnValue(target=TOW_Tug)
    t1.start()
    print(t1.join())
    #tt = .15    #.12 is "normal" ppl type speed, higher means slower
    amPlayingGame=False

TOW_INCDEC_AMT = 0.0

def incOrDecBy(GameRegion):
    global TOW_INCDEC_AMT
    extremeAmt = -.008
    slowAmt = .04
    #I feel there is a better way than how I am doing it,
    #but I will first check for too slow or too fast and return relative to that
    
    while TOW_isRunning:
        if py.locateOnScreen(curDirPlus(TOW_TOOFAST),confidence=.7) is not None:
            TOW_INCDEC_AMT = slowAmt
        elif py.locateOnScreen(curDirPlus(TOW_TOOSLOW),confidence=.7) is not None:
            TOW_INCDEC_AMT = extremeAmt
        else:
            TOW_INCDEC_AMT = -0.00073
        #time.sleep(.25)

    #once done, set this to 0 for next time 
    TOW_INCDEC_AMT = 0.0

class ThreadWithReturnValue(Thread):
    def __init__(self, group=None, target=None, name=None,
                 args=(), kwargs={}, Verbose=None):
        Thread.__init__(self, group, target, name, args, kwargs)
        self._return = None
    def run(self):
        #print(type(self._target))
        if self._target is not None:
            self._return = self._target(*self._args,
                                                **self._kwargs)
    def join(self, *args):
        Thread.join(self, *args)
        return self._return

def TOW_Tug():
    w = (SCREEN_WIDTH)/2
    h = SCREEN_HEIGHT
    xOffset = (SCREEN_WIDTH / 10)
    GameRegion = (int(w-(w/6)),int(h-(h-(h/10))), 320, 400)
    GameOverRegion = (xOffset,(SCREEN_HEIGHT - (SCREEN_HEIGHT / 5)), SCREEN_WIDTH - (2 * xOffset), SCREEN_HEIGHT - (SCREEN_HEIGHT - (SCREEN_HEIGHT / 5)))
    normalamt = .3
    
    #t2 = threading.Thread(target=incOrDecBy,args=[GameRegion])
    #t3 = threading.Thread(target=TOW_isGameOver,args=[GameOverRegion])
    t3 = ThreadWithReturnValue(target=TOW_isGameOver, args=(GameOverRegion,))
    t3.start()
    t2 = ThreadWithReturnValue(target=incOrDecBy, args=(GameRegion,))
    t2.start()
    while(TOW_isRunning):
        
        normalamt += TOW_INCDEC_AMT
        if(normalamt<0):
            normalamt=0.01
        elif(normalamt>1.2):
            normalamt=.7
        keyboard.press('a')
        keyboard.release('a')
        time.sleep(normalamt)
        keyboard.press('d')
        keyboard.release('d')

    print(t3.join())
    return "Done Tugging"
    
def TOW_isGameOver(gameOverRegion):
    global TOW_isRunning
    count = 0
    while(TOW_isRunning):
        if py.locateOnScreen(curDirPlus(TUG_O_WAR_GAMEOVER), confidence=.8):
            TOW_isRunning = False   #to stop the tugging
            print("Good Game")
            return True
        else:
            time.sleep(5)
            count+=1
            if count > 10:          #time slept times this num is full seconds waited
                TOW_isRunning=False     
                print("Something went wrong")
        
    return False

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#Everything below this line is the process of looping around to navigate the screen to play games if found in list of games known to play
#add game play above this section as this section will be last


#Directory Stuff


def curDirPlus(filename):
    filestuff = os.path.join('Trolley', os.path.join('images', filename))        #this part is for me, as my current working directory is further back (will change when I change cwd)
    return os.path.join(os.getcwd(),filestuff)

def curDirMem(filename):
    filestuff = os.path.join('Trolley', os.path.join(r'images\MemGame', filename))        #this part is for me, as my current working directory is further back (will change when I change cwd)
    return os.path.join(os.getcwd(),filestuff)

#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
#||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||||
def waitForBeans():
    dabeans = py.locateOnScreen(curDirPlus(GETTING_BEANS),confidence=.75)
    while dabeans is None:
        time.sleep(1)
        dabeans = py.locateOnScreen(curDirPlus(GETTING_BEANS),confidence=.75)

def afterGame():
    """Loops indefinitly as playingGameTypeAgain is True"""
    global playingGameTypeAgain
    #first wait until it is on jellybean page
    beans = py.locateOnScreen(curDirPlus(GETTING_BEANS),confidence=.7)
    while beans is None:
        time.sleep(.5)
        beans = py.locateOnScreen(curDirPlus(GETTING_BEANS),confidence=.7)

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
    while not cc:
        time.sleep(.5)
        cc = py.locateOnScreen(curDirPlus(SKIP_BUTTON))
    py.moveTo(cc)
    py.click()
    time.sleep(1.4)


def checkIfOnTrolley():

    winsound.Beep(100,300)
    findMe = py.locateOnScreen(curDirPlus(TROLLEY),confidence=.8)
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
