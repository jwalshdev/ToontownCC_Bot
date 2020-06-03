import pyautogui as py
import time, os

DELAY_BETWEEN_COMMANDS = 1
GAG_MENU = 'Gag_Shop_Menu.PNG'
TU_START_GAG = 'ToonUp_Sart_Gag.PNG'
GAG_MENU_EXIT_BUTTON = 'Done_Buying.PNG'
FRIENDS_BUTTON = 'Friends_Button.PNG'
TOONUP_LEVEL=0
TRAP_LEVEL=0
LURE_LEVEL=3
SOUND_LEVEL=4
SQUIRT_LEVEL=5
ZAP_LEVEL=5
THROW_LEVEL=0
DROP_LEVEL=0

TOONUP_GAGS=[0]
TRAP_GAGS=[0]
LURE_GAGS=[0,0,0]
SOUND_GAGS=[0,0,2,3]
SQUIRT_GAGS=[0,2,2,2,3]
ZAP_GAGS=[0,2,2,2,3]
THROW_GAGS=[0]
DROP_GAGS=[0]


MyGags = [TOONUP_GAGS, TRAP_GAGS, LURE_GAGS, SOUND_GAGS, SQUIRT_GAGS, ZAP_GAGS, THROW_GAGS, DROP_GAGS]
#for amount of gags I have

MyGagLevel = [TOONUP_LEVEL, TRAP_LEVEL, LURE_LEVEL, SOUND_LEVEL, SQUIRT_LEVEL, ZAP_LEVEL, THROW_LEVEL, DROP_LEVEL]
#for amount of levels of this gag track i have

"""this GagLevelLimit is for when the toon is maxed, as it is different per level"""
#GagLevelLimit = [10, 10, 10, 10, 7, 5, 3, 1]

#for the limiting max gags you can buy
TU_LIMIT=[]
TRAP_LIMIT=[]
LURE_LIMIT=[]
SOUND_LIMIT=[]
SQUIRT_LIMIT=[]
ZAP_LIMIT=[]
THROW_LIMIT=[]
DROP_LIMIT=[]

GagLevelLimit = [TU_LIMIT,TRAP_LIMIT, LURE_LIMIT, SOUND_LIMIT, SQUIRT_LIMIT, ZAP_LIMIT, THROW_LIMIT, DROP_LIMIT]

GagList = ['ToonUp', 'Trap','Lure','Sound','Squirt','Zap','Throw','Drop']


"""
Exit Button: 1436,598
Toonup box info:
(First Gag)
    Top left: 700,250
    Bottom Left: 700,290
    Top Right: 770, 250
    Bottom Right: 770, 290

offset of maybe 5 
(Second Gag)

Trap info:
    Top Left: 700,300
"""

#IDEA: have image search to see where I am so it auto picks the playground
#At start, input the street wanted and that will walk accordingly to what playground and street inputted

def main():
    #Initial position is from gag shop
    #GameCountdown initializes everything
    gameCountdown()
    isGameOn()
    #getGagLevels()  
        #this will open up the book in the bottom right and open up to gag page if not already on
        #Then it will scan to see what levels are for what
    #getCurrentGagAmount()
        #Will eventually check through the book and get amount of gags currently have
    """When buying gags, have a maxLevel buying limit to buy based on this max level"""
    
    walkToGagClerk()
    time.sleep(1.1)
    #swipeGags()
    buyAllGagsNeeded()
    time.sleep(1)
    leaveGagClerk()
    time.sleep(3)
    fromGagToWackyWay()

def isGameOn():
    game = py.locateOnScreen(curDirPlus(FRIENDS_BUTTON))
    if game is None:
        raise Exception("Game not found, is it on the main screen?")
    print("Game found....Welcome to Toontown!")
    
def buyByType(type):
    print('hello')

def buyAllGagsNeeded():
    startLoc = py.locateOnScreen(curDirPlus(TU_START_GAG))
    if startLoc is None:
        print("Not at the menu")
        resetTalkingToClerk()
        return
    x = startLoc[0] + 150       #starting pos x and y are determined based on screen resolution, these best fit me 
    y = startLoc[1] + 20        #later I will try to find a way to work for all while not just searching for the first box's image (for performance)
    dx, dy = 80, 50     #these should be ok as they are
    thisgagtrack=None

    for i in range(0, 8):
        x=startLoc[0] + 150
        if MyGagLevel[i] > 0:
            x+=(dx * (MyGagLevel[i]-1))     #Now x is at the last gag level with that gag track
            print("Gag level of: " + str(MyGagLevel[i]) )
            #buy until the limit is reached or until bag is full (or really safe until time is exceeded)
            thisgagtrack = MyGags[i]
            amountAtEnd = thisgagtrack[-1]
            #this is the amount we have so far


            while amountAtEnd < GagLevelLimit[i][-1]:
                py.click(x,y)
                print("Clicked with amount of: " + str(amountAtEnd))
                time.sleep(.1)
                amountAtEnd+=1
        y+=dy

    #assuming gags are all bought and good, go to exit button and leave
    exit = py.locateOnScreen(curDirPlus(GAG_MENU_EXIT_BUTTON))
    if exit is None:
        print("Someone kicked you out of the menu somehow, welp time to leave")
        #leaveGagClerk()
        return
    print("Gags purchased, time to leave")
    py.moveTo(exit)
    py.click()
    time.sleep(1)
    moveBy('s',.3)
    
def leaveGagClerk():
    print("hello")
    turnAround()
    moveBy('w',4)

def turnAround():
    moveBy('d',1.5)
    

def swipeGags():
    #swipes through all gags
    startLoc = py.locateOnScreen(curDirPlus(TU_START_GAG))
    if startLoc is None:
        print("Not at the menu")
        resetTalkingToClerk()
        return
    x = startLoc[0] + 150       #starting pos x and y are determined based on screen resolution, these best fit me 
    y = startLoc[1] + 20        #later I will try to find a way to work for all while not just searching for the first box's image (for performance)
    dx, dy = 80, 50     #these should be ok as they are
    thisgagtrack=None


    for i in range(0,8):
        for j in range(0,8):
            py.moveTo(x,y,duration=.2)
            x+=dx
        x=startLoc[0] + 150
        y+=dy
    

def walkToGagClerk():
    moveBy('d',.25)
    moveBy('w',2)

    """This could lead to problems later on, as"""
    #if someone is currently trading already when I walk up to the counter and I still have to trade
    #Solution: while value is true and the trade menu isnt open (if it is open then it is overrided)
    #this might be able to be done in a function-> CheckIfTrading(bool val)
    #CheckIfTrading checks if it still has to trade (passing this hasToTrade value through) or if the menu is open
    hasToTrade = True

    while hasToTrade:
        if py.locateOnScreen(curDirPlus(GAG_MENU)) is not None:
            hasToTrade = False
            print("Gag Menu Found")
            time.sleep(1.3)
            return
        print("Gag menu not found, Trying again")
        time.sleep(1)
        resetTalkingToClerk()

def resetTalkingToClerk():
    moveBy('s',1)
    time.sleep(.1)
    moveBy('w',1)


def CheckIfTrading():
    #prerequisite: hasToTrade is True
    shopFound = False
    menucoords = py.locateOnScreen(curDirPlus(GAG_MENU))
    if menucoords is not None:
        return True
    return False

def fromGagToWackyWay():
    #walks forward
    moveBy('w',2)
    #Turn left to face Wacky Way
    moveBy('a',.43)
    #Walk forward into WW
    moveBy('w',8)
    #now we will be in wacky way

def moveBy(key, amount):
    py.keyDown(key)
    time.sleep(amount)
    py.keyUp(key)

def gameCountdown():
    #initial of the game
    py.FAILSAFE=True

    print("Starting",end="")
    for i in range(0,5):
        print(".",end="")
        time.sleep(1)
    print("Go")

def getGagInputs():
    #temporary until I can run a bot to scan it all
    word = ''
    for i in range(0,len(MyGags)):
        MyGags[i] = input("Enter amount of " + GagList[i] + " gags currently owned: ")
        MyGags[i]-=1

def curDirPlus(filename):
    #This takes from Python Scripts to the trolley
    filestuff = os.path.join(r'AdvancedScripts\TTCC\GagTraining', os.path.join('images', filename))        #this part is for me, as my current working directory is further back (will change when I change cwd)
    return os.path.join(os.getcwd(),filestuff)

def calculateGagLimits():
    """
TOONUP_LEVEL=0
TRAP_LEVEL=0
LURE_LEVEL=3
SOUND_LEVEL=4
SQUIRT_LEVEL=5
ZAP_LEVEL=5
THROW_LEVEL=0
DROP_LEVEL=0

Limits[]
GagLevelLimit[]
    """
    """
    (may be different here with corporate clash, as this is from ttr)
    Limit from a maxed gagtrack: 30,25,20,15,7,3,1
    when level is 8 (max) is 30,25,20,15,7,3,1
    when level is 7 it is 30,25,20,15,7,3
    6 is ?? (probably 25,20,15,10,7,3)
    5 is 25,20,15,10,3
    4 is 20,15,10,5
    3 is 15,10,5
    2 is 10,5
    1 is 10
    """
    
    for i in range(0,8):
        if MyGagLevel[i] > 0:
            if MyGagLevel[i] == 1:
                GagLevelLimit[i] = [10]
            elif MyGagLevel[i] == 2:
                GagLevelLimit[i] = [10,5]
            elif MyGagLevel[i] == 3:
                GagLevelLimit[i] = [15,10,5]
            elif MyGagLevel[i] == 4:
                GagLevelLimit[i] = [20,15,10,5]
            elif MyGagLevel[i] == 5:
                GagLevelLimit[i] = [25,20,15,10,3]
            elif MyGagLevel[i] == 6:
                GagLevelLimit[i] = [25,20,15,10,7,3]
            elif MyGagLevel[i] == 7:
                GagLevelLimit[i] = [30,25,20,15,7,3]
            elif MyGagLevel[i] == 8:
                GagLevelLimit[i] = [30,25,20,15,7,3,1]
        else:
            GagLevelLimit[i] = [None]


if __name__ == "__main__":
    #getGagInputs()
    #calculateGagLimits()
    #main()
    