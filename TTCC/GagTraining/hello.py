import winsound, time
import tkinter as tk
def main(): 
    frequency = 500  # Set Frequency To 2500 Hertz
    duration = 500  # Set Duration To 1000 ms == 1 second
    #winsound.Beep(frequency, duration)
    countdownSounds()
    #checkMouseRightScreen()
    root = tk.Tk()

    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()

    print(screen_height)
    print(screen_width)

def countdownSounds():
    frequency = 500  
    duration = 500
    for i in range(0,3):
        winsound.Beep(frequency,duration)
        time.sleep(.5)
    frequency=1000
    duration=600
    winsound.Beep(frequency,duration)

if __name__ == "__main__":
    main()