import pyautogui as py
import time

def main():
    time.sleep(3)
    while True:
        time.sleep(5)
        clickMe('space', .2)
        time.sleep(2)
        
def clickMe(key, timeframe):
    py.keyDown(key)
    time.sleep(timeframe)
    py.keyUp(key)

if __name__ == "__main__":
    main()