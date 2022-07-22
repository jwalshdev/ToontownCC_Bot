import time

from TTCC.GagTraining.Battle import checkIfFighting, battle
from TTCC.GagTraining.GagShop import walkToGagClerk, buyByType, leaveGagClerk
from TTCC.GagTraining.Movement import fromGagToSeaweedStreet, toBattleSpot, fromBattleSpot, toGagFromSeaweedStreet, \
    moveBy
from TTCC.GagTraining.Helpers import gameCountdown, isGameOn, isHealthy


def main():
    gameCountdown()
    isGameOn()
    walkToGagClerk()
    time.sleep(1.1)
    buyByType("sound")
    time.sleep(1)
    leaveGagClerk()
    time.sleep(3)
    fromGagToSeaweedStreet()
    time.sleep(10)
    toBattleSpot()
    while not checkIfFighting():
        print("Waiting for battle...")
        time.sleep(5)
    battle()
    fromBattleSpot()
    time.sleep(10)
    toGagFromSeaweedStreet()


def run():
    while True:
        t1 = time.time()
        main()
        while not isHealthy():
            print("Not healthy... waiting")
            time.sleep(5)
            moveBy('end', .5)
        print(f"TIME: {time.time() - t1}")


if __name__ == "__main__":
    run()
