import CombatSystem
import EquipmentSystem
import DungeonCrawl
import Texts
import os
import time
import random
import copy



def startGame():
    gamerunning = True

    while gamerunning == True:
        # GAME BOOTS DIRECTLY INTO DUNGEON CRAWL
        # HERE THE STORY AND OTHER THINGS WILL GO TOWARDS AFTER.    

        if CombatSystem.gameover(CombatSystem.party):
            gamerunning = False
            break

        os.system("cls")
        # DungeonCrawl.exploreDungeon()
        from TownSystem import runTown
        runTown()

startGame()

###