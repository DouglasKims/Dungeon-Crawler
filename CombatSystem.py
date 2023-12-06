# create dice rolling functions
# create a turn based combat system

import math
import os
import time
import random
import copy
import CharacterSystem
import EnemyGenerator

import EnemyList


# COLORS
BLACK = "\033[30m"
RED = "\033[31m"
GREEN = "\033[32m"
YELLOW = "\033[33m"
BLUE = "\033[34m"
MAGENTA = "\033[35m"
CYAN = "\033[36m"
WHITE = "\033[37m"
RESET = "\033[0m"  # Reset to default color

# Bright versions
BRIGHT_BLACK = "\033[90m"
BRIGHT_RED = "\033[91m"
BRIGHT_GREEN = "\033[92m"
BRIGHT_YELLOW = "\033[93m"
BRIGHT_BLUE = "\033[94m"
BRIGHT_MAGENTA = "\033[95m"
BRIGHT_CYAN = "\033[96m"
BRIGHT_WHITE = "\033[97m"

# Background colors (add 10 to the color code)
BG_BLACK = "\033[40m"
BG_RED = "\033[41m"
BG_GREEN = "\033[42m"
BG_YELLOW = "\033[43m"
BG_BLUE = "\033[44m"
BG_MAGENTA = "\033[45m"
BG_CYAN = "\033[46m"
BG_WHITE = "\033[47m"

cclasses = CharacterSystem.character_classes

""" 0: Phys
    1: fire
    2: wind
    3: earth
    4: ice
    5: thunder
    6: toxic
"""

elem = ["phys","fire","wind","earth","ice","thunder","toxic","decay","chaos","death"]


enemies_1 = EnemyList.enemies_1
enemies_bosses = EnemyList.enemies_bosses

party = CharacterSystem.party
opposition = []

atkmod = 0
d100 = 0
dmgdice = 0
damage = 0
miss = False
enemytarget = None
chartarget = None
charcommand = None
rounds = 0
atk_report = ""


def rollattack(char,target):
    global atk_report
    global atkmod
    global d100
    global miss
    miss = False
    d100 = random.randint(1,100)

    # print (d100)
    if d100 >= 90 * abs((math.sqrt(int(char.lck))/100)-(math.sqrt(int(char.agi))/100)+1):
        print(f"Miss!")
        # print(f"Miss! // Miss Thresh: {90 * abs((math.sqrt(int(char.lck))/100)-(math.sqrt(int(char.agi))/100)+1)}")
        atkmod = 0
        miss = True
    ## FUMBLE MECHANIC
    # elif d100 >= 80 + math.sqrt(round(char.lck)):
    #         print(f"Fumble! (0.5x damage)")
    #         # print(f"Fumble! (0.5x damage) // F.Thresh: {80 + math.sqrt(round(char.lck))}")
    #         atkmod = 0.5
    else:
        if d100 <= int(char.lck)/2 + int(char.agi)/4:
            print(f"Critical Hit! ({round(1.5 + (int(char.lck)/100),1)}x damage)")
            # print(f"Critical Hit! (1.5x damage) // Crit.Thresh: {(int(char.lck)/2 + int(char.agi)/4)}")
            atkmod = 1.5 + (int(char.lck)/100)
        else:
            atkmod = 1

    atk_report += f"atkmod {atkmod}, "
    return atkmod

def rolldamage(char):
    global atk_report
    rolleddamage = 0
    for _ in range(int(char.str)):
        if char.dmg == 1:
            rolleddamage += random.randint(1,4) # 1d4 / AVG 2,5
        elif char.dmg == 2:
            rolleddamage += random.randint(1,6) # 1d6 / AVG 3,5
        elif char.dmg == 3:
            rolleddamage += random.randint(1,8) # 1d8 / AVG 4,5
        elif char.dmg == 4:
            rolleddamage += random.randint(2,12) # 2d6 / AVG 7
        elif char.dmg == 5:
            rolleddamage += random.randint(2,16) # 2d8 / AVG 9
        elif char.dmg == 6:
            rolleddamage += random.randint(2,20) # 2d10 / AVG 11
        elif char.dmg == 7:
            rolleddamage += random.randint(3,24) # 3d8 / AVG 13,5
        elif char.dmg == 8:
            rolleddamage += random.randint(3,30) # 3d10 / AVG 16,5
        elif char.dmg == 9:
            rolleddamage += random.randint(3,36) # 3d12 / AVG 19,5
        elif char.dmg >= 10:
            rolleddamage += random.randint(4,40) # 4d10 / AVG 22


    rolleddamage = rolleddamage
    atk_report += f"Rolled dmg {rolleddamage}, "
    return rolleddamage

def attackfunc(attacker,target):
    global opptoremove
    global atk_report
    atk_report = ""
    rollattack(attacker,target)

    atk_report += f"Attacker STR: {attacker.str} (Sqrd. {round(math.sqrt(attacker.str))}), "
    atk_report += f"Defender VIT {target.vit} (Sqrd. {abs(round(math.sqrt(target.vit)/10-1))}), "

    finaldamage = round((((rolldamage(attacker)) * atkmod) * (math.sqrt(attacker.str)/10+1) + attacker.str) * abs(math.sqrt(target.vit)/10-1))
    
    atk_report += f"\nFinal calc'd damaged: {finaldamage} dealt by {attacker.name}."

    if miss == True:
        finaldamage = 0

    if finaldamage > 0:
        if "phys" in target.weak:
            finaldamage = finaldamage * 1.5
            print (f"{attacker.name} attacks {target.name}, who's weak to Physical attacks for {finaldamage} damage!")

        elif "phys" in target.resist:
            finaldamage = int(finaldamage * 0.5)
            print (f"{attacker.name} attacks {target.name}, who's resistant to Physical attacks for {finaldamage} damage!")

        elif target.defending == True:
            finaldamage = finaldamage // 2
            print (f"{attacker.name} attacks {target.name}, but they defended and suffered only {finaldamage} damage.")

        else:
            print (f"{attacker.name} attacks {target.name} for {finaldamage} damage.")

        target.hp -= finaldamage
        if target.hp <= 0 and target in party:
            print (f"{target.name} has been downed!")
            target.hp = 0
        if target in party and target.hp > 0:
            print (f"{target.name}'s HP: {math.floor(target.hp)} / {math.floor(target.maxhp)}")

    

    elif finaldamage <= 0:
        print (f"{attacker.name} attacks {target.name}, but causes no damage.")

    if target.hp <= 0 and target in opposition:
        opposition.remove(target)
        opptoremove.append(target)
        print (f"{attacker.name} defeated {target.name}!")

    # print (atk_report)

def fetchSkills(char):
    
    spellchart = {
        "firo": "fire",
        "gelo": "ice",
        "gale": "wind",
        "tera": "earth",
        "volt": "thunder",
        "veno": "toxic",
        "nuke": "chaos"
        }

    availableskills = ""
    availableskills_sup = ""
    availableskills_phys = ""
    print (f"\n{char.name} knows:")

    # FOR loop / For "X" in spell, print an f-string with proper names

    for element in ["firo", "gelo", "gale", "tera", "volt", "veno", "nuke"]:
        if element in char.slist:
            availableskills += f" {element.upper()} (weak {spellchart[element]} damage to one target // 4 TP)\n"
        
        if f"grun{element}" in char.slist:
            availableskills += f" GRUN{element.upper()} (weak {spellchart[element]} damage to all targets // 10 TP)\n"
        if f"{element}mor" in char.slist:
            availableskills += f" {element.upper()}MOR (medium {spellchart[element]} damage to one target // 8 TP)\n"
        if f"grun{element}mor" in char.slist:
            availableskills += f" GRUN{element.upper()}MOR (medium {spellchart[element]} damage to all targets // 16 TP)\n"
        if f"{element}matha" in char.slist:
            availableskills += f" {element.upper()}MATHA (heavy {spellchart[element]} damage to one target // 12 TP)\n"
        if f"grun{element}matha" in char.slist:
            availableskills += f" GRUN{element.upper()}MATHA (heavy {spellchart[element]} damage to all targets // 22 TP)\n"

    if availableskills != "":
        print ("ELEMENTAL skills")
        print (availableskills)

    # if "firo" in char.slist:
    #     availableskills += " FIRO (weak fire damage to one target // 4 TP)\n"
    # if "grunfiro" in char.slist:
    #     availableskills += " GRUNFIRO (weak fire damage to all targets // 10 TP)\n"
    # if "firomor" in char.slist:
    #     availableskills += " FIROMOR (medium fire damage to one target // 8 TP)\n"
    # if "grunfiromor" in char.slist:
    #     availableskills += " GRUNFIROMOR (medium fire damage to all targets // 16 TP)\n"
    # if "firomatha" in char.slist:
    #     availableskills += " FIROMATHA (heavy fire damage to one target // 12 TP)\n"
    # if "grunfiromatha" in char.slist:
    #     availableskills += " GRUNFIROMATHA (heavy fire damage to all targets // 22 TP)\n"
    
    if "cura" in char.slist:
        availableskills_sup += " CURA (Restores a low amount of HP to one ally // 3 TP)\n"
    if "gruncura" in char.slist:
        availableskills_sup += " GRUNCURA (Restores a low amount of HP to all allies // 7 TP)\n"
    if "curamor" in char.slist:
        availableskills_sup += " CURAMOR (Restores a medium amount of HP to one ally // 7 TP)\n"
    if "gruncuramor" in char.slist:
        availableskills_sup += " GRUNCURAMOR (Restores a low amount of HP to all allies // 12 TP)\n"
    if "curamatha" in char.slist:
        availableskills_sup += " CURA (Fully restores HP to one ally // 18 TP)\n"
    if "gruncuramatha" in char.slist:
        availableskills_sup += " GRUNCURA (Fully restores HP to all allies // 30 TP)\n"

    
    if "revita" in char.slist:
        availableskills_sup += f" REVITA (Revives a fallen ally with 30% of HP // 7 TP)\n"
    if "revitamor" in char.slist:
        availableskills_sup += f" REVITAMOR (Revives a fallen ally with 60% of HP // 10 TP)\n"

    if availableskills_sup != "":
        print("SUPPORT Skills")
        print(availableskills_sup)

    if "charge" in char.slist:
        availableskills_phys += f" CHARGE (Attacks one enemy up to three times // {round(char.maxhp*0.15)} HP)\n"

    if "cleave" in char.slist:
        availableskills_phys += f" CLEAVE (Attack random enemies up to five times // {round(char.maxhp*0.20)} HP and 4 TP)\n"

    if "sneak" in char.slist:
        availableskills_phys += f" SNEAK (Attacks one enemy with increased damage and crit chance // 4 TP)\n"
    
    if availableskills_phys != "":
        print("PHYSICAL Skills")
        print(availableskills_phys)


def command(char):
    global chartarget
    global opposition
    global charcommand

    availablecommands = "(A)ttack, (D)efend, (S)kills, (U)pdate list"

    if char.char_class.name == "Knight":
        availablecommands += ", (C)harge, Cleave, Hunt"

    if char.char_class.name == "Scout":
        availablecommands += ", Sneak"

    availablecommands += ", (or type a combination of skills to use them)"

    charcommand = input(f"What is {char.name} doing?\n {availablecommands}\n").lower()

    if charcommand == "attack" or charcommand == "a":

        chartarget = targetenemy()

        if chartarget is not None:

            attackfunc(char,chartarget)
            
            char.acted = True

            
        pass

    elif charcommand == "defend" or charcommand == "d":
        char.defending = True
        print (f"{char.name} is defending.")

        char.acted = True
        pass

    elif charcommand == "skill" or charcommand == "skills" or charcommand == "s":
        fetchSkills(char)
        
# PHYS SKILLS

    elif charcommand == "charge" or charcommand == "c":
        if char.char_class.name == "Knight" and char.hp > round(char.maxhp*0.15):
            chartarget = targetenemy()

            if chartarget is not None:

                char.hp -= round(char.maxhp*0.15)
                attacktimes = random.randint(1,3)

                for _ in range (1,attacktimes+1):

                    attackfunc(char,chartarget)

                    if chartarget.hp <= 0:
                        break
                    time.sleep(0.6)

                char.acted = True
        
        else:
            print (f"{char.name} can't use this skill.")

    elif charcommand == "cleave" or charcommand == "f":
        if char.char_class.name == "Knight" and char.hp > round(char.maxhp*0.25):
            
            attacktimes = random.randint(1,5)
            char.hp -= round(char.maxhp*0.25)

            for _ in range(attacktimes):
                if opposition:
                    chartarget = random.choice(opposition)
                    attackfunc(char,chartarget)
                    time.sleep(0.6)

                    char.acted = True
                
        else:
            print (f"{char.name} can't use this skill.")

    elif charcommand == "hunt":
        if char.char_class.name == "Knight" and char.hp > round(char.maxhp*0.15) and char.tp >= 3:
            chartarget = targetenemy()

            if chartarget is not None:

                char.hp -= round(char.maxhp*0.15)
                char.tp -= 3

                char.str += 3
                char.lck += 20
                attackfunc(char,chartarget)
                char.str -= 3
                char.lck -= 20

                char.acted = True
        
        else:
            print (f"{char.name} can't use this skill.")

    elif charcommand == "sneak":
        if char.char_class.name == "Scout" and char.tp >= 3:
            chartarget = targetenemy()

            if chartarget is not None:

                char.tp -= 3

                char.str += 1
                char.dmg += 1
                char.lck += 20
                attackfunc(char,chartarget)
                char.dmg -= 1
                char.str -= 1
                char.lck -= 20

                char.acted = True

# ELEM SKILLS
    elif "leas" in charcommand:
        if "leas" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,None)

    elif "pas" in charcommand:
        if "pas" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"fire")

    elif "yab" in charcommand:
        if "yab" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"thunder")

    elif "gaa" in charcommand:
        if "gaa" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"earth")

    elif "hak" in charcommand:
        if "hak" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"decay")

    elif "igg" in charcommand:
        if "igg" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"toxic")

    elif "irg" in charcommand:
        if "irg" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"ice")

    elif "fam" in charcommand:
        if "fam" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"air")

    elif "khos" in charcommand:
        if "khos" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"chaos")



    elif "firo" in charcommand:
        if "firo" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"fire")

    elif "volt" in charcommand:
        if "volt" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"thunder")

    elif "tera" in charcommand:
        if "tera" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"earth")

    elif "veno" in charcommand:
        if "veno" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"toxic")

    elif "gelo" in charcommand:
        if "gelo" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"ice")

    elif "gale" in charcommand:
        if "gale" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"air")

    elif "nuke" in charcommand:
        if "nuke" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,"chaos")

# SUPPORT SKILLS
    elif "cura" in charcommand:
        if "cura" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,None)

    elif "revita" in charcommand:
        if "revita" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            spellversion(char,charcommand,None)

    



    elif "update" in charcommand or "u" in charcommand:
        updatecombatlist()

    elif "rush" in charcommand: # FINISH
        rushcount = int(input("How many turns to rush? (0 to cancel) "))

    elif "die" in charcommand:
        char.hp = 0
        print(f"{char.name} feel dead.")
        char.acted = True

    else:
        print("Invalid command or character can't use this skill.")

def usetp(char,tp):
    if char.tp < tp:
        print(f"{char.name} doesn't have enough TP.")
        cancast = False
    else:
        char.tp -= tp
        cancast = True
    return cancast

def calcspelldamage(char,spelllevel):
    global spelldamage
    spelldamage = 0
    if spelllevel == "weak":
        for _ in range(int(char.tec)):
            spelldamage += random.randint(2,8) # 2d4 / AVG 5
    elif spelllevel == "medium":
        for _ in range(int(char.tec)):
            spelldamage += random.randint(4,16) # 4d4 / AVG 10
    elif spelllevel == "heavy":
        for _ in range(int(char.tec)):
            spelldamage += random.randint(6,24) # 6d4 / AVG 15

def calcspellheal(char,spelllevel):
    spellheal = 0
    if spelllevel == "weak":
        spellheal = 25 * (math.sqrt(int(char.tec))/10+1)
    elif spelllevel == "medium":
        spellheal = 50 * (math.sqrt(int(char.tec))/10+1)
    elif spelllevel == "heavy":
        spellheal = 100

    return spellheal

def spellversionold(char,spell,dmgtype):
    starget = None
    if "lag" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usetp(char,10) == True:
                calcspelldamage(char,"weak")
                usespell(char,starget,dmgtype,"multi")

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usetp(char,4) == True:
                starget = targetenemy()
                if starget is not None:
                    calcspelldamage(char,"weak")
                    usespell(char,starget,dmgtype,"single")
        pass

    elif "comas" in spell and "comas" in char.slist:
        if "grun" in spell and "grun" in char.slist:
            if usetp(char,16) == True:
                calcspelldamage(char,"medium")
                usespell(char,starget,dmgtype,"multi")

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usetp(char,8) == True:
                starget = targetenemy()
                if starget is not None:
                    calcspelldamage(char,"medium")
                    usespell(char,starget,dmgtype,"single")

        pass

    elif "asmatha" in spell and "asmatha" in char.slist:
        if "grun" in spell and "grun" in char.slist:
            if usetp(char,22) == True:
                calcspelldamage(char,"heavy")
                usespell(char,starget,dmgtype,"multi")

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usetp(char,12) == True:
                starget = targetenemy()
                if starget is not None:
                    calcspelldamage(char,"heavy")
                    usespell(char,starget,dmgtype,"single")

        #cast hvy
        pass

    elif "tin" in spell and not "igg" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usetp(char,7) == True:
                heal = calcspellheal(char,"weak")
                for n in party:
                    # healally function
                    healally(char,n,heal)

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usetp(char,3) == True:
                starget = targetally()
                if starget is not None:
                    heal = calcspellheal(char,"weak")
                    healally(char,starget,heal)
        pass

    elif "cruai" in spell and "cruai" in char.slist and not "igg" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usetp(char,12) == True:
                heal = calcspellheal(char,"medium")
                for n in party:
                    # healally function
                    healally(char,n,heal)

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usetp(char,7) == True:
                starget = targetally()
                if starget is not None:
                    heal = calcspellheal(char,"medium")
                    healally(char,starget,heal)
        pass

    elif "fallain" in spell and "fallain" in char.slist and not "igg" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usetp(char,30) == True:
                heal = calcspellheal(char,"heavy")
                for n in party:
                    # healally function
                    healally(char,n,heal)

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usetp(char,18) == True:
                starget = targetally()
                if starget is not None:
                    heal = calcspellheal(char,"heavy")
                    healally(char,starget,heal)
        pass

    elif "igg" in spell and "tin" in spell:
        if "igg" in char.slist:
            
            if usetp(char,7) == True:
                starget = targetdeadally()
                if starget is not None:
                    starget.hp += round((starget.maxhp*30/100))

                    print (f"{starget.name} has been revived with {round(starget.maxhp*30/100)} HP!")
                    char.acted = True

    elif "igg" in spell and "cruai" in spell:
        if "igg" in char.slist and "cruai" in char.slist:

            if usetp(char,10) == True:
                starget = targetdeadally()
                if starget is not None:
                    starget.hp += round((starget.maxhp*60/100))

                    print (f"{starget.name} has been revived with {round(starget.maxhp*60/100)} HP!")
                    char.acted = True

    elif "igg" in spell and "fallain" in spell:
        if "igg" in char.slist and "fallain" in char.slist:
            if usetp(char,18) == True:
                starget = targetdeadally()
                if starget is not None:
                    starget.hp += round((starget.maxhp))

                    print (f"{starget.name} has been revived with full HP!")
                    char.acted = True

    else:
        print(f"{char.name} can't use this skill.")

def spellversion(char,spell,dmgtype):
    starget = None

    if "cura" not in spell and "revita" not in spell and any(element in spell for element in ["firo", "gelo", "gale", "tera", "volt", "veno", "nuke"]):

        if "mor" in spell and spell in char.slist:
            if "grun" in spell and spell in char.slist:
                if usetp(char,16) == True:
                    calcspelldamage(char,"medium")
                    usespell(char,starget,dmgtype,"multi")

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            elif spell in char.slist:
                if usetp(char,8) == True:
                    starget = targetenemy()
                    if starget is not None:
                        calcspelldamage(char,"medium")
                        usespell(char,starget,dmgtype,"single")

            pass

        elif "matha" in spell and spell in char.slist:
            if "grun" in spell and "grun" in char.slist:
                if usetp(char,22) == True:
                    calcspelldamage(char,"heavy")
                    usespell(char,starget,dmgtype,"multi")

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            elif spell in char.slist:
                if usetp(char,12) == True:
                    starget = targetenemy()
                    if starget is not None:
                        calcspelldamage(char,"heavy")
                        usespell(char,starget,dmgtype,"single")

        elif "mor" not in spell and "matha" not in spell and "cura" not in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,10) == True:
                    calcspelldamage(char,"weak")
                    usespell(char,starget,dmgtype,"multi")

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            elif spell in char.slist:
                if usetp(char,4) == True:
                    starget = targetenemy()
                    if starget is not None:
                        calcspelldamage(char,"weak")
                        usespell(char,starget,dmgtype,"single")

        else:
            print(f"{char.name} can't use this skill.")

    elif "cura" in spell:
        if "cura" in spell and "mor" in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,12) == True:
                    heal = calcspellheal(char,"medium")
                    for n in party:
                        # healally function
                        healally(char,n,heal)

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            else:
                if usetp(char,7) == True:
                    starget = targetally()
                    if starget is not None:
                        heal = calcspellheal(char,"medium")
                        healally(char,starget,heal)
            pass

        elif "cura" in spell and "matha" in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,30) == True:
                    heal = calcspellheal(char,"heavy")
                    for n in party:
                        # healally function
                        healally(char,n,heal)

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            else:
                if usetp(char,18) == True:
                    starget = targetally()
                    if starget is not None:
                        heal = calcspellheal(char,"heavy")
                        healally(char,starget,heal)
            pass

        elif "cura" in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,7) == True:
                    heal = calcspellheal(char,"weak")
                    for n in party:
                        # healally function
                        healally(char,n,heal)

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            else:
                if usetp(char,3) == True:
                    starget = targetally()
                    if starget is not None:
                        heal = calcspellheal(char,"weak")
                        healally(char,starget,heal)

        else:
            print(f"{char.name} can't use this skill.")

    elif "revita" in spell:
        
        if "revita" in spell and "mor" not in spell and "motha" not in spell:
            if spell in char.slist:
                
                if usetp(char,7) == True:
                    starget = targetdeadally()
                    if starget is not None:
                        starget.hp += round((starget.maxhp*30/100))

                        print (f"{starget.name} has been revived with {round(starget.maxhp*30/100)} HP!")
                        char.acted = True

        elif "revita" in spell and "mor" in spell:
            if spell in char.slist:

                if usetp(char,10) == True:
                    starget = targetdeadally()
                    if starget is not None:
                        starget.hp += round((starget.maxhp*60/100))

                        print (f"{starget.name} has been revived with {round(starget.maxhp*60/100)} HP!")
                        char.acted = True

        elif "revita" in spell and "motha" in spell:
            
            if spell in char.slist:
                if usetp(char,18) == True:
                    starget = targetdeadally()
                    if starget is not None:
                        starget.hp = round((starget.maxhp))

                        print (f"{starget.name} has been revived with full HP!")
                        char.acted = True
        
        else:
            print(f"{char.name} can't use this skill.")

    


def updatecombatlist():
    global rounds
    os.system("cls")
    print (f"Round {rounds}")
    print ("") #spacer
    print ("Party:") #spacer
    for n in party:
        if n.hp <= 0:
            print (f"({party.index(n)}) {BG_RED}{n.name}{RESET}'s HP: DEAD/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        else:
            print (f"({party.index(n)}) {n.name}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
    print ("") #spacer
    print ("Opposition") #spacer
    for n in opposition:
        print (f"({opposition.index(n)}) Level {n.level} {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")
    print ("") #spacer
    initnames = ", ".join(str(n.name) for n in initiative)
    print (f"Turn order: {initnames}\n")


## Logic

cancelterms = ["no","back","cancel","return","quit"]

def targetenemy():
    starget = None
    stargetindex = None

    if len(opposition) == 1:
        target = opposition[0]
        quickattack = input(f"Attack {target.name}? (\"No\" to cancel)").lower()
        if quickattack in cancelterms:
            return None
        else:
            return target

    while stargetindex == None:
        
        stargetindex = input("Who are you targeting? ")
        
        if stargetindex in cancelterms or stargetindex == "":
            print("")
            return None

        try:
            stargetindex = int(stargetindex)
        except ValueError:
            continue

        if stargetindex in range(0,len(opposition)):
            starget = opposition[int(stargetindex)]
        else:
            print("Invalid target.")
            stargetindex = None    

    target = starget
    return target

def targetally():
    stargetindex = None
    while stargetindex == None:

        stargetindex = input("Who are you targeting? ")

        if stargetindex in cancelterms or stargetindex == "":
            print("")
            return None
        
        try:
            stargetindex = int(stargetindex)
        except ValueError:
            continue

        if stargetindex in range(0,len(party)) and party[stargetindex].hp > 0:
            starget = party[int(stargetindex)]
        else:
            print("Invalid target.")
            stargetindex = None
    target = starget
    return target

def targetdeadally():
    stargetindex = None
    while stargetindex == None:

        stargetindex = input("Who are you targeting? ")

        if stargetindex in cancelterms  or stargetindex == "":
            print("")
            return None

        try:
            stargetindex = int(stargetindex)
        except ValueError:
            continue

        if stargetindex in range(0,len(party)) and party[stargetindex].hp <= 0:
            starget = party[int(stargetindex)]
        else:
            print("Invalid target.")
            stargetindex = None
    target = starget
    return target

def healally(char, n, heal):
    if n.hp > 0:
        n.hp += round((n.maxhp*heal/100))

        print (f"{n.name} has been healed for {round(n.maxhp*heal/100)}")

        if n.hp > n.maxhp:
            n.hp = n.maxhp
    else:
        print(f"No effect on {n.name}")

    char.acted = True

def usespell(char,starget,dmgtype,spelltype):
    global spelldamage
    global opptoremove
    defeatedopp = []
    defeatedparty = []

    # Use tp and roll damage
    # char.tp -= tpcost
    # spelldamage = 0
    # for _ in range(char.tec):
    #     spelldamage += random.randint(1,6)

    if spelltype == "single":
        dealspelldamage(char,starget,dmgtype,spelldamage)
        if starget.hp <= 0:
            if starget in opposition:
                opposition.remove(starget)
                opptoremove.append(starget)
                print (f"{char.name} defeated {starget.name}!")
            
            # elif starget in party:
            #     print (f"{char.name} downed {starget.name}!")

    elif spelltype == "multi":
        if char in party:
            for n in opposition:
                dealspelldamage(char,n,dmgtype,spelldamage)
                if n.hp <= 0:
                    defeatedopp.append(n)
        elif char in opposition:
            for n in party:
                dealspelldamage(char,n,dmgtype,spelldamage)
                if n.hp <= 0:
                    defeatedparty.append(n)
        

        print("")
        for n in defeatedopp:
            print (f"{char.name} defeated {n.name}!")
            opposition.remove(n)
            opptoremove.append(n)
            pass
        for n in defeatedparty:
            print (f"{char.name} defeated {n.name}!")
            pass

    if starget in party:
        if starget.hp <= 0:
            print (f"{starget.name} has been downed!")
            starget.hp = 0
    if starget in party and starget.hp > 0 and spelltype == "single":
        print (f"{starget.name}'s HP: {starget.hp} / {starget.maxhp}")
    
    if char in party:
        char.acted = True

def dealspelldamage(char,starget,dmgtype,spelldamage):

    # Reduce target's TEC from damage
        # (SQRT(TEC) - 1)*-1
    spelldamage = abs(round(spelldamage * (math.sqrt(char.tec)/10+1) * ((math.sqrt(starget.tec)/10-1))))

    # LCK to evade spell
    sd100 = random.randint(1,100)
    
    if sd100 <= math.sqrt(starget.lck)/100:
        print (f"{starget.name} managed to avoid the attack!")

    else:
        if dmgtype in starget.weak:
            spelldamage = round(spelldamage * (1.5 + math.sqrt(char.tec)/10+1))
            print (f"{starget.name} is weak to {dmgtype} and suffered {spelldamage} {dmgtype} damage!")
        
        elif starget.defending == True:
            spelldamage = round(spelldamage * (math.sqrt(char.tec)/10+1))//2
            print (f"{starget.name} was defending and suffered only {spelldamage} {dmgtype} damage.")

        elif dmgtype in starget.resist:
            spelldamage = round(spelldamage * (math.sqrt(char.tec)/10+1)//1.5)
            print (f"{starget.name} is resistant to {dmgtype} and suffers only {spelldamage} {dmgtype} damage.")

        else:
            print (f"{starget.name} suffered {spelldamage} {dmgtype} damage.")
        starget.hp -= spelldamage

    if starget in party and starget.hp <= 0:
        starget.hp = 0

def gameover(party):
    global isgameover
    isgameover = True
    return all(n.hp == 0 for n in party)

opptoremove = []
combat_money = 0
combat_exp = 0
# Find party level

def partyLevel():
    plevel = 0
    for n in party:
        plevel += n.level

    plevel = round(plevel / len(party))
    return plevel
    
def calcenemyexp(enemy):
    global combat_exp
    plevel = partyLevel()

    if "Làidir" in enemy.name:
        combat_exp += round(round(40*enemy.level/plevel) * 10)
    else:
        combat_exp += round(40*enemy.level/plevel)

def endofturncleanup():
    global initiative
    global opptoremove
    global combat_exp
    global combat_money

    for n in opptoremove:
        calcenemyexp(n)
        combat_money += n.money

        if n in initiative:
            initiative.remove(n)

    opptoremove = []

def calcRewards():
    global combat_exp
    global combat_money
    
    party_money = CharacterSystem.party_money

    aliveparty = 0
    for n in party:
        if n.hp >0:
            aliveparty += 1
    
    # combat_exp = round(combat_exp // aliveparty)

    for n in party:
        if n.hp >0:
            n.exp += combat_exp
    
    CharacterSystem.party_money += combat_money

## initiative system
initiative = []
initnames = []

def rollinitiative():
    global initiative
    global initnames

    initiative = []
    initdict = {}

    for n in party:
        initroll = random.randint(1,10)+n.agi
        initdict.update({n: initroll})
    for n in opposition:
        initroll = random.randint(1,10)+n.agi
        initdict.update({n: initroll})


    sortedinit = sorted(initdict.items(), key=lambda item: item[1], reverse=True)

    initiative = [item[0] for item in sortedinit]

    renamed_init = renameduplicates(initiative)

    initiative = renamed_init
                
def renameduplicates(initlist):
    ids = ["A","B","C","D","E","F"]
    name_counts = {}
    for n in initlist:
        if n not in party:
            name_count = name_counts.get(n.name, 0)
            name_counts[n.name] = name_count + 1
            
            if name_count == 0:
                n.name = f"{YELLOW}{n.name} {ids[name_count]}{RESET}"
            if name_count > 0:
                n.name = f"{YELLOW}{n.name} {ids[name_count]}{RESET}"

    # for n in initlist:
    #     uniqueidindex = 0
    #     if initiative.count(char) > 1:
    #         for char in initiative:
    #             char.name += f" {ids[uniqueidindex]}"
    #             uniqueidindex += 1
    
    return initlist

def randomenemies():
    global opposition
    global bossbattle

    # 10% of boss
    if 'bossbattle' in globals() and bossbattle:
        laidirBattle = 1
    else:
        laidirBattle = random.randint(2,100)

    if laidirBattle > 1:

        # Level adequate enemies
        levelmodifier = random.choice([0.5,1,2,3,4])
        enemygrouplevel = int(partyLevel() * levelmodifier)

        while enemygrouplevel > 0:
            # enemy_to_add = copy.deepcopy(random.choice(enemies_1))
            # opposition.append(enemy_to_add)
            # enemygrouplevel -= enemy_to_add.level


            randomenemylevel = partyLevel() + random.randint(-2,2) -1 
            if randomenemylevel < 0:
                randomenemylevel = 0

            entype = random.choice(["Malla","Sgeu","Diogh","Colt","Adhbah","Grain"])

            enemy_to_add = EnemyGenerator.generateEnemy(entype,randomenemylevel)
            opposition.append(enemy_to_add)
            enemygrouplevel -= enemy_to_add.level

            if len(opposition) >5:
                break

        if not opposition:
            entype = random.choice(["Malla","Sgeu","Diogh","Colt","Adhbah","Grain"])
            opposition.append(EnemyGenerator.generateEnemy(entype,partyLevel()))
            
    
    else:
        print("A Làidir has appeared!")
        opposition.append(copy.deepcopy(random.choice(enemies_bosses)))

    bossbattle = False

dioghtarget = None

def enemyTurn(enemy):
    global enemytarget
    global dioghtarget
    
    choice = None
    enemytarget = None
    
    if "Diogh" in enemy.name:
        if not dioghtarget:

            while enemytarget == None or enemytarget.hp == 0 or dioghtarget.hp == 0:
                enemytarget = random.choice(party)
                print (f"{enemy.name} seems fixated on {enemytarget.name}...")
                dioghtarget = enemytarget
        else:
            enemytarget = dioghtarget

    # TARGET
    while enemytarget == None or enemytarget.hp == 0:
        enemytarget = random.choice(party)

    # PHYS OR ELEM?
    physweight = enemy.str
    elemweight = enemy.tec
    enemychoices = ["phys","elem","aoeelem"]

    # THESE will NEVER attack physically
    if "Adhbah" in enemy.name or "Grain" in enemy.name:
        # choice = random.choices(["elem","aoeelem"], weights=[2,1], k=1)[0]
        physweight = 0
    # THESE will NEVER cast spells
    elif "Malla" in enemy.name or "Sgeu" in enemy.name or "Diogh" in enemy.name:
        elemweight = 0
    
    # else:
    #     choice = random.choices(enemychoices, weights=[physweight,elemweight,elemweight/2], k=1)[0]

    choice = random.choices(enemychoices, weights=[physweight,elemweight,elemweight/2], k=1)[0]

    if choice == "phys":
        attackfunc(enemy,enemytarget)

    elif choice == "elem":
        if enemy.level < 5:
            spelllevel = "weak"
            enemy.tp -= 4
        elif enemy.level < 10 :
            spelllevel = "medium"
            enemy.tp -= 7
        

        if enemy.tp < 0:
            print (f"{enemy.name} tried to use a technique, but couldn't focus.")
            attackfunc(enemy,enemytarget)
        else:
            dmgtype = elem[random.randint(1,6)]

            calcspelldamage(enemy,spelllevel)
            usespell(enemy,enemytarget,dmgtype,"single")

    elif choice == "aoeelem":
    
        if enemy.level < 5:
            spelllevel = "weak"
            enemy.tp -= 4
        elif enemy.level < 10 :
            spelllevel = "medium"
            enemy.tp -= 7

        if enemy.tp < 0:
            print (f"{enemy.name} tried to use a technique, but couldn't focus.")
            attackfunc(enemy,enemytarget)
        else:
            dmgtype = elem[random.randint(1,6)]

            calcspelldamage(enemy,spelllevel)
            usespell(enemy,enemytarget,dmgtype,"multi")


    pass


plevel_exp = [0,500,1000,1500,2000,5000,12000]

        
# GAME
def runCombat():
    global combat_money
    global combat_exp
    global rounds
    global dioghtarget

    randomenemies()
    rollinitiative()
    initnames = ", ".join(str(n.name) for n in initiative)
    print (f"Turn order: {initnames}")

    rounds = 0
    testing_combat = True
    while testing_combat:

        os.system('cls')

        if not opposition:
            testing_combat = False
            calcRewards()
            print(f"You won the combat in {rounds} rounds!\nThe party gains {combat_money} Cr and each living party member receives {combat_exp} experience.")
            combat_money = 0
            combat_exp = 0
            input("Type anything to continue: ")
            for n in party:
                CharacterSystem.checkLevel(n)
            
            return
            # break

        rounds += 1
        updatecombatlist()
        
        print ("") #spacer

        for n in initiative:
            if n not in party and n.hp <= 0:
                pass
            else:
                print(f"It's {n.name}'s turn!")
            if n in party and n.hp <= 0:
                print (f"But they're down.")
                print ("")

            if n in opposition and n.hp > 0:

                enemyTurn(n)
                # enemytarget = None
                # while enemytarget == None or enemytarget.hp == 0:
                #     enemytarget = random.choice(party)
                # attackfunc(n,enemytarget)

                #game over function
                if gameover(party):
                    print ("")
                    print ("All heroes have been defeated.")
                    break

                print ("")
                time.sleep(0.8)
            
            elif n in party:
                n.acted = False
                n.defending = False
                if not opposition:
                    pass
                elif n.hp <= 0:
                    pass
                else:
                    while n.acted == False:
                        command(n)

                    print ("")
                    time.sleep(0.8)

        if gameover(party):
            print ("")
            print ("Game Over.")
            break

        endofturncleanup()

        input("Type anything to continue: ")
    
    dioghtarget = None


# TESTING
# runCombat()


# Create PHYS skills for non-casters (buffs, defense, physical attacks)
    # Multi-hit variant for all enemies
    # Medium/Heavy damage variants
    # High crit rate attack