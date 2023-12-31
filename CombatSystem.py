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
            finaldamage = round(finaldamage * 1.5)
            print (f"{attacker.name} attacks {target.name}, who's weak to Physical attacks for {finaldamage} damage!")

        elif "phys" in target.resist:
            finaldamage = int(finaldamage * 0.5)
            print (f"{attacker.name} attacks {target.name}, who's resistant to Physical attacks for {finaldamage} damage!")

        elif target.defending == True:
            finaldamage = finaldamage // 2
            print (f"{attacker.name} attacks {target.name}, but they defended and suffered only {finaldamage} damage.")

        else:
            print (f"{attacker.name} attacks {target.name} for {finaldamage} damage.")

        if "protect" in target.effects:
            finaldamage = int (finaldamage * ( 1 - target.effects["protect"][0] * 0.05 ) )
            print (f"But! {target.name} was protected and suffered only {finaldamage} damage.")

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
    
    availableskills = ""
    availableskills_sup = ""
    availableskills_phys = ""
    print (f"\n{char.name} knows:")

    for n in char.slist:
        if len(char.slist[n]) < 4:
            availableskills += f" {n.upper()} Level {char.slist[n][0]}: {char.slist[n][1]} // {char.slist[n][2]} TP \n"


    if availableskills != "":
        print ("ELEMENTAL skills")
        print (availableskills)

    for n in char.slist:
        if len(char.slist[n]) > 3 and char.slist[n][3] == "S":
            availableskills_sup += f" {n.upper()} Level {char.slist[n][0]}: {char.slist[n][1]} // {char.slist[n][2]} TP \n"

    if availableskills_sup != "":
        print("SUPPORT Skills")
        print(availableskills_sup)
    
    for n in char.slist:
        if len(char.slist[n]) > 3 and char.slist[n][3] != "S":
            if char.slist[n][3] > 0:
                if char.slist[n][2] > 0:
                    availableskills_phys += f" {n.upper()} Level {char.slist[n][0]}: {char.slist[n][1]} // {char.slist[n][2]} TP / {char.maxhp * int(char.slist[n][3])//100} HP\n"
                else:
                    availableskills_phys += f" {n.upper()} Level {char.slist[n][0]}: {char.slist[n][1]} // {char.maxhp * int(char.slist[n][3])//100} HP\n"
            else:
                availableskills_phys += f" {n.upper()} Level {char.slist[n][0]}: {char.slist[n][1]} // {char.slist[n][2]} TP\n"


    if availableskills_phys != "":
        print("PHYSICAL Skills")
        print(availableskills_phys)


def command(char):
    global chartarget
    global opposition
    global charcommand

    availablecommands = "(A)ttack, (D)efend, (I)tem, (S)kills, (U)pdate list, (E)scape"

    if char.char_class.name == "Knight":
        availablecommands += ", Charge, Cleave, Protect"

    if char.char_class.name == "Scout":
        availablecommands += ", Sneak, Hunt, Decoy"

    availablecommands += ", (or type a combination of elemental skills to use them)"

    charcommand = ""
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

    elif charcommand == "i" or charcommand == "item":
        from EquipmentSystem import consumables
        from EquipmentSystem import useItem
        usingitem = True
        while usingitem:
            print("Consumables:")
            for n in  consumables:
                print (f" ({consumables.index(n)}) {n.name} // Type: {n.type} // Effect: {n.lore} // Value: {n.value} Cr")

            useitem = input(f"\nAre you using any item? If so, type the consumable number, otherwise press anything.\n")

            try:
                useitem = int(useitem)
            except ValueError:
                useitem = None

            if useitem in range(0,len(consumables)):
                print("using item")
                print("")
                if useItem(consumables[useitem]) == True:
                    char.acted = True
            
            usingitem = False


# PHYS SKILLS
    elif charcommand == "charge":
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

    elif charcommand == "cleave":
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
        if char.char_class.name == "Scout" and char.tp >= 5:
            chartarget = targetenemy()

            if chartarget is not None:

                char.tp -= 5

                strbonus = ((math.sqrt(chartarget.hp)/10+1) * char.str) - char.str

                char.str += strbonus
                attackfunc(char,chartarget)
                char.str -= strbonus

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

    elif "bomb" in charcommand:
        if "bomb" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            if usetp(char,char.slist["bomb"][2]) == True:
                global opptoremove
                defeatedopp = []
                bombdamage = int( char.slist["bomb"][0] * (math.sqrt(char.lck)/10+1) * 15 ) # Bomb power = 15

                for enemy in opposition:
                    enemy.hp -= bombdamage
                    print (f"{enemy.name} suffered {bombdamage} explosion damage.")
                    if enemy.hp <= 0:
                            defeatedopp.append(enemy)

                print (" ")
                for n in defeatedopp:
                    print (f"{char.name} defeated {enemy.name}!")
                    opposition.remove(enemy)
                    opptoremove.append(enemy)

                char.acted = True


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

    elif charcommand == "protect":
        from CombatEffects import applyEffect

        if "protect" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            if usetp(char,char.slist[charcommand][2]) == True:
                    for n in party:
                        applyEffect(char,charcommand,n)

            char.acted = True
            pass

    elif "decoy" in charcommand:

        if char.tp >= 15 and charcommand in char.slist:
            
            decoy = CharacterSystem.Character(
                name=f"{char.name}'s Decoy", char_class="Decoy", race = None,
                level=1, maxhp=(25*char.slist["decoy"][0]), hp=(25*char.slist["decoy"][0]), maxtp=0, tp=0,
                str=0, dmg=0, tec=(2*char.slist["decoy"][0]), vit=(3*char.slist["decoy"][0]), agi=(2*char.slist["decoy"][0]), lck=0,
                acted=False, defending=False, weak=[], resist=[], exp=0, init=0, skillpts=0, perkpts=0,
                equip={
                "Weapon":None,
                "Armor":None,
                "Accessory 1":None,
                "Accessory 2":None},
                slist={}
                )

            
            for n in party:
                if n.name == f"{char.name}'s Decoy":
                    party.remove(n)
            party.append(copy.deepcopy(decoy))
            
            char.acted = True
            os.system("cls")
            updatecombatlist()
            pass

        else:
            "Not enough TP."

    elif "enha" in charcommand:
        from CombatEffects import applyEffect
        
        if charcommand in char.slist:
            if "grun" in charcommand:
                if usetp(char,char.slist[charcommand][2]) == True:
                    for n in party:
                        applyEffect(char, charcommand, n)
                    char.acted = True
            else:
                if usetp(char,char.slist[charcommand][2]) == True:
                    target = targetally()
                    applyEffect(char, charcommand, target)
                    char.acted = True
        else:
            print (f"{n.name} can't use this skill.")

    elif "enfe" in charcommand:
        from CombatEffects import applyEffect
        
        if charcommand in char.slist:
            if "grun" in charcommand:
                if usetp(char,char.slist[charcommand][2]) == True:
                    for enemy in opposition:
                        applyEffect(char, charcommand, enemy)
                    char.acted = True
            else:
                if usetp(char,char.slist[charcommand][2]) == True:
                    target = targetenemy()
                    applyEffect(char, charcommand, target)
                    char.acted = True
        else:
            print (f"{n.name} can't use this skill.")

    elif charcommand == "coating":
        from CombatEffects import applyEffect

        if "coating" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            if usetp(char,char.slist[charcommand][2]) == True:
                for n in party:
                    applyEffect(char,charcommand,n)

                char.acted = True
            pass

    elif charcommand == "appraise":
        from CombatEffects import applyEffect

        if "appraise" not in char.slist:
            print(f"{char.name} can't use this skill.")
        else:
            if usetp(char,char.slist[charcommand][2]) == True:
                enemy = targetenemy()

                enemy.exp += 0.25 * char.slist["appraise"][0]

                char.acted = True
            pass

    elif "update" in charcommand or "u" in charcommand:
        updatecombatlist()

    elif "rush" in charcommand: # FINISH
        rushcount = int(input("How many turns to rush? (0 to cancel) "))

    elif "escape" in charcommand or charcommand == "e": # FINISH
        chance = 30 + char.agi
        escaped100 = random.randint(1,100)

        if escaped100 <= chance:
            opposition.clear()
            
            input (f"The group escapes!")
            char.acted = True

        else:
            input (f"Failed to escape.")
            char.acted = True
            pass

    elif "die" in charcommand:
        char.hp = 0
        print(f"{char.name} feel dead.")
        char.acted = True


    else:
        print("Invalid command.")

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
                if usetp(char,char.slist[spell][2]) == True:
                    calcspelldamage(char,"medium")
                    usespell(char,starget,dmgtype,"multi")

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            elif spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetenemy()
                    if starget is not None:
                        calcspelldamage(char,"medium")
                        usespell(char,starget,dmgtype,"single")

            pass

        elif "matha" in spell and spell in char.slist:
            if "grun" in spell and "grun" in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    calcspelldamage(char,"heavy")
                    usespell(char,starget,dmgtype,"multi")

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            elif spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetenemy()
                    if starget is not None:
                        calcspelldamage(char,"heavy")
                        usespell(char,starget,dmgtype,"single")

        elif "mor" not in spell and "matha" not in spell and "cura" not in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    calcspelldamage(char,"weak")
                    usespell(char,starget,dmgtype,"multi")

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            elif spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetenemy()
                    if starget is not None:
                        calcspelldamage(char,"weak")
                        usespell(char,starget,dmgtype,"single")

        else:
            print(f"{char.name} can't use this skill.")

    elif "cura" in spell:
        if "cura" in spell and "mor" in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    heal = calcspellheal(char,"medium")
                    for n in party:
                        # healally function
                        healally(char,n,heal)

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            else:
                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetally()
                    if starget is not None:
                        heal = calcspellheal(char,"medium")
                        healally(char,starget,heal)
            pass

        elif "cura" in spell and "matha" in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    heal = calcspellheal(char,"heavy")
                    for n in party:
                        # healally function
                        healally(char,n,heal)

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            else:
                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetally()
                    if starget is not None:
                        heal = calcspellheal(char,"heavy")
                        healally(char,starget,heal)
            pass

        elif "cura" in spell:
            if "grun" in spell and spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
                    heal = calcspellheal(char,"weak")
                    for n in party:
                        # healally function
                        healally(char,n,heal)

            elif "grun" in spell and spell not in char.slist:
                print(f"{char.name} can't use this skill.")

            else:
                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetally()
                    if starget is not None:
                        heal = calcspellheal(char,"weak")
                        healally(char,starget,heal)

        else:
            print(f"{char.name} can't use this skill.")

    elif "revita" in spell:
        
        if "revita" in spell and "mor" not in spell and "motha" not in spell:
            if spell in char.slist:
                
                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetdeadally()
                    if starget is not None:
                        starget.hp += round((starget.maxhp*30/100))

                        print (f"{starget.name} has been revived with {round(starget.maxhp*30/100)} HP!")
                        char.acted = True

        elif "revita" in spell and "mor" in spell:
            if spell in char.slist:

                if usetp(char,char.slist[spell][2]) == True:
                    starget = targetdeadally()
                    if starget is not None:
                        starget.hp += round((starget.maxhp*60/100))

                        print (f"{starget.name} has been revived with {round(starget.maxhp*60/100)} HP!")
                        char.acted = True

        elif "revita" in spell and "motha" in spell:
            
            if spell in char.slist:
                if usetp(char,char.slist[spell][2]) == True:
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
        if n.hp <= 0 and n.char_class != "Decoy":
            print (f"({party.index(n)}) {BG_RED}{n.name}{RESET}'s HP: DEAD/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        elif n.char_class == "Decoy":
            print (f"({party.index(n)}) {CYAN}{n.name}{RESET}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
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
        
    for n in opposition:
        print (f"({opposition.index(n)}) Level {n.level} {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")

    while stargetindex == None:
        
        stargetindex = input("Who are you targeting? ")
        
        if stargetindex in cancelterms or stargetindex == "":
            print("")
            return None

        try:
            stargetindex = int(stargetindex)
        except ValueError:
            continue
        except:
            continue

        if stargetindex in range(0,len(opposition)):
            starget = opposition[int(stargetindex)]
        else:
            print("Invalid target.")
            stargetindex = None    

    return starget

def targetally():
    stargetindex = None
    starget = None

    for n in party:
        if n.hp <= 0 and n.char_class != "Decoy":
            print (f"({party.index(n)}) {BG_RED}{n.name}{RESET}'s HP: DEAD/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        elif n.char_class == "Decoy":
            print (f"({party.index(n)}) {CYAN}{n.name}{RESET}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        else:
            print (f"({party.index(n)}) {n.name}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")

    while stargetindex == None:

        stargetindex = input("Who are you targeting? ")

        if stargetindex in cancelterms or stargetindex == "":
            print("")
            return None
        
        try:
            stargetindex = int(stargetindex)
        except ValueError:
            continue
        except:
            continue

        if stargetindex in range(0,len(party)) and party[stargetindex].hp > 0:
            starget = party[int(stargetindex)]
        else:
            print("Invalid target.")
            stargetindex = None
    
    return starget

def targetdeadally():
    stargetindex = None
    starget = None

    for n in party:
        if n.hp <= 0 and n.char_class != "Decoy":
            print (f"({party.index(n)}) {BG_RED}{n.name}{RESET}'s HP: DEAD/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        elif n.char_class == "Decoy":
            print (f"({party.index(n)}) {CYAN}{n.name}{RESET}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        else:
            print (f"({party.index(n)}) {n.name}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")

    while stargetindex == None:

        stargetindex = input("Who are you targeting? ")

        if stargetindex in cancelterms or stargetindex == "":
            print("")
            return None

        try:
            stargetindex = int(stargetindex)
        except ValueError:
            continue
        except:
            continue

        if stargetindex in range(0,len(party)) and party[stargetindex].hp <= 0:
            starget = party[int(stargetindex)]
        else:
            print("Invalid target.")
            stargetindex = None

    return starget

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
    
    spelldamage = round(spelldamage * (math.sqrt(char.tec)/10+1))
    

    if sd100 <= math.sqrt(starget.lck)/100:
        print (f"{starget.name} managed to avoid the attack!")

    else:
        if dmgtype in starget.weak:
            spelldamage = int (spelldamage * 1.5)
            print (f"{starget.name} is weak to {dmgtype} and suffered {spelldamage} {dmgtype} damage!")

        elif starget.defending == True:
            spelldamage = spelldamage // 2
            print (f"{starget.name} was defending and suffered only {spelldamage} {dmgtype} damage.")

        elif dmgtype in starget.resist:
            spelldamage = spelldamage // 1.5
            print (f"{starget.name} is resistant to {dmgtype} and suffers only {spelldamage} {dmgtype} damage.")

        else:
            print (f"{starget.name} suffered {spelldamage} {dmgtype} damage.")

        if "protect" in starget.effects:
            spelldamage = int (spelldamage * ( 1 - starget.effects["protect"][0] * 0.05 ) )
            print (f"But! {starget.name} was protected and suffered only {spelldamage} {dmgtype} damage.")

        if "coating" in starget.effects:
            if dmgtype in ("fire","wind","earth","ice","thunder","toxic","decay","chaos"):
                spelldamage = int (spelldamage - ( spelldamage * math.sqrt(starget.effects["protect"][0])/10) )
                print (f"But! {starget.name} was coated and suffered only {spelldamage} {dmgtype} damage.")

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
        combat_exp += round(round(40*enemy.level/plevel) * 10) * enemy.exp
    else:
        combat_exp += round(40*enemy.level/plevel) * enemy.exp

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

    for char in party:
        if char.char_class == "Decoy" and n.hp <= 0:
            party.remove(char)


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

    combatCleanup()

def combatCleanup():
    # Remove Decoys
    for n in party:
        if n.char_class == "Decoy":
            party.remove(n)

        n.effects.clear()

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
        opposition.append(EnemyGenerator.generateEnemy("Laidir",partyLevel()))

    bossbattle = False

dioghtarget = None

def enemyTurn(enemy):
    global enemytarget
    global dioghtarget
    
    choice = None
    enemytarget = None
    dmgtype = None
    
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
        if enemy.level < 6:
            spelllevel = "weak"
            enemy.tp -= 4
        elif enemy.level < 12 :
            spelllevel = "medium"
            enemy.tp -= 7
        

        if enemy.tp < 0:
            print (f"{enemy.name} tried to use a technique, but couldn't focus.")
            attackfunc(enemy,enemytarget)
        else:
            if len(enemy.resist) != 0:
                dmgtype = random.choice(enemy.resist)
            else:
                while dmgtype in enemy.weak or dmgtype == None:
                    dmgtype = elem[random.randint(1,6)]

            calcspelldamage(enemy,spelllevel)
            usespell(enemy,enemytarget,dmgtype,"single")

    elif choice == "aoeelem":
    
        if enemy.level < 6:
            spelllevel = "weak"
            enemy.tp -= 10
        elif enemy.level < 12 :
            spelllevel = "medium"
            enemy.tp -= 16

        if enemy.tp < 0:
            print (f"{enemy.name} tried to use a technique, but couldn't focus.")
            attackfunc(enemy,enemytarget)
        else:
            if len(enemy.resist) != 0:
                dmgtype = random.choice(enemy.resist)
            else:
                while dmgtype in enemy.weak or dmgtype == None:
                    dmgtype = elem[random.randint(1,6)]
                

            calcspelldamage(enemy,spelllevel)
            usespell(enemy,enemytarget,dmgtype,"multi")


    pass


        
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
            print(f"You won the combat in {rounds} rounds!\nThe party gains {combat_money} Cr and each living party member receives {int(combat_exp)} experience.")
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

                if len(n.effects) > 0:
                    for effect in n.effects:
                        from CombatEffects import tickEffect
                        tickEffect(n)


                enemyTurn(n)


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

                    if len(n.effects) > 0:
                        effect_keys = list(n.effects.keys())
                        for effect in effect_keys:
                            from CombatEffects import tickEffect
                            tickEffect(n)

                    while n.acted == False:
                        
                        if len(n.effects) > 0:
                            print("Active Effects:")
                            effect_keys = list(n.effects.keys())
                            for effect in effect_keys:
                                print(f"{effect.upper()}: boost: {int(n.effects[effect][0])} / turns left: {n.effects[effect][1]}")

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
