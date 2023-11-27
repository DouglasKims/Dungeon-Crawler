# create dice rolling functions
# create a turn based combat system

import math
import os
import time
import random
import copy

import EnemyList

class Character:
    def __init__(self,name,char_class,level,plevel,maxhp,hp,maxfp,fp,str,dmg,tec,vit,agi,lck,slist,acted,defending,weak,equip,exp,init):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.plevel = plevel
        self.maxhp = maxhp
        self.hp = hp
        self.maxfp = maxfp
        self.fp = fp
        self.str = str
        self.dmg = dmg
        self.tec = tec
        self.vit = vit
        self.agi = agi
        self.lck = lck
        self.slist = slist
        self.acted = acted
        self.defending = defending
        self.weak = weak
        self.equip = equip
        self.exp = exp
        self.init = init

# Class Enemy:

class CharacterClass:
    def __init__(self,name,hp,fp,str,dmg,tec,vit,agi,lck,special,lore):
        self.name = name
        self.hp = hp
        self.fp = fp
        self.str = str
        self.dmg = dmg
        self.tec = tec
        self.vit = vit
        self.agi = agi
        self.lck = lck
        self.special = special
        self.lore = lore

# CHARACTER CLASSES
#   # KNIGHT
knight = CharacterClass(
    name = "Knight",
    hp = 10,
    fp = 2,
    str = 6,
    dmg = 2,
    tec = 2,
    vit = 5,
    agi = 3,
    lck = 3,
    special = None,
    lore = "A capable fighter with high attack and defense, know a few combat tactics, but doesn't excels in special techniques.")
#   # THAUMATURGE
thaumaturge = CharacterClass(
    "Thaumaruge",
    hp = 6,
    fp = 5,
    str = 4,
    dmg = 1,
    tec = 6,
    vit = 2,
    agi = 2,
    lck = 4,
    special = None,
    lore = "A capable combatant who's reliable in physical combat, but really excells at support and healing.")
#   # ARCANIST
arcanist = CharacterClass(
    "Arcanist",
    hp = 4,
    fp = 7,
    str = 2,
    dmg = 1,
    tec = 8,
    vit = 1,
    agi = 4,
    lck = 2,
    special = None,
    lore = "A specialist combatant, really weak and fragile, but can use devastating special techniques and elemental attacks.")
#   # SCOUT
scout = CharacterClass(
    "Scout",
    hp = 6,
    fp = 3,
    str = 3,
    dmg = 2,
    tec = 4,
    vit = 2,
    agi = 8,
    lck = 8,
    special = None,
    lore = "A stealthy combatant, somewhat weak and fragile, but capable of landing powerful critical attacks more frequently than others.")
#   # SCHOLAR
scholar = CharacterClass(
    "Scholar",
    hp = 8,
    fp = 4,
    str = 5,
    dmg = 1,
    tec = 5,
    vit = 3,
    agi = 5,
    lck = 5,
    special = None,
    lore = "A well-rounded combatant and explorer, able to use offensive and support abilities, but doesn't really excels in any.")
#   # QUARTERMASTER
quartermaster = CharacterClass(
    "Quartermaster",
    hp = 6,
    fp = 3,
    str = 4,
    dmg = 1,
    tec = 2,
    vit = 4,
    agi = 5,
    lck = 5,
    special = None,
    lore = "A supportive combatant, not very powerful in combat, but able to make exploration easier with many support skills.")

cclasses = [knight,thaumaturge,arcanist,scout,scholar,quartermaster]

""" 0: Phys
    1: fire
    2: wind
    3: earth
    4: ice
    5: thunder
    6: toxin
"""

elem = ["phys","fire","wind","earth","ice","thunder","toxic","decay","chaos","death"]

drav_equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None
}
dan_equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None
}
mars_equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None
}

dravspells = ["leas","pas","comas","grun"]
danspells = ["leas","cruai","igg","gaa","grun","comas"]
marsspells = ["leas","yab","grun"]


drav = Character("Dravroth","Bard",1,1,80,80,40,40,6,1,6,2,5,6,dravspells,False,False,[],drav_equip,0,0)
dan = Character("Thorudan","Thaumaturge",1,1,80,80,50,50,4,1,10,2,3,3,danspells,False,False,[],dan_equip,0,0)
mars = Character("Mars","Knight",1,1,100,100,20,20,8,2,3,4,3,3,marsspells,False,False,[],mars_equip,0,0)
eck = Character(
    name="Eckbert",
    char_class="Scout",
    level=1,plevel=1,
    maxhp=60, hp=60, maxfp=30, fp=30, str=3, dmg=2, tec=4, vit=2, agi=8, lck=8,
    slist=[], acted=False, defending=False, weak=[], exp=0, init=0,
    equip={
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None
    })



enemies_1 = EnemyList.enemies_1


party = [drav,dan,mars,eck]
party_money = 0
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



def rollattack(char,target):
    global atkmod
    global d100
    global miss
    miss = False
    d100 = random.randint(1,100)

    if d100 >= 90 * abs((math.sqrt(char.lck)/100)-(math.sqrt(char.agi)/100)+1):
        print("Miss!")
        atkmod = 0
        miss = True
    elif d100 >= 80 + math.sqrt(char.lck)/100:
            print("Fumble!")
            atkmod = 0.5
    else:
        if d100 <= char.lck/2 + char.agi/4:
            print("Critical Hit!")
            atkmod = 1.5 + (char.lck/100)
        else:
            atkmod = 1

    return atkmod

def rolldamage(char):
    rolleddamage = 0
    for _ in range(char.str):
        if char.dmg == 1:
            rolleddamage += random.randint(1,4)
        elif char.dmg == 2:
            rolleddamage += random.randint(2,6)
        elif char.dmg == 3:
            rolleddamage += random.randint(3,8)
        elif char.dmg >= 4:
            rolleddamage += random.randint(4,10)

    rolleddamage = rolleddamage
    return rolleddamage

def attackfunc(attacker,target):
    global opptoremove

    rollattack(attacker,target)

    finaldamage = round((rolldamage(attacker)) * atkmod) # - (target.vit * target.level))
    
    if miss == True:
        finaldamage = 0

    if finaldamage > 0:
        if "phys" in target.weak:
            finaldamage = finaldamage * 2
            print (f"{attacker.name} attacks {target.name}, who's weak to Physical attacks for {finaldamage} damage!")

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
            print (f"{target.name}'s HP: {target.hp} / {target.maxhp}")


    elif finaldamage <= 0:
        print (f"{attacker.name} attacks {target.name}, but causes no damage.")

    if target.hp <= 0 and target in opposition:
        opposition.remove(target)
        opptoremove.append(target)
        print (f"{attacker.name} defeated {target.name}!")

def command(char):
    global chartarget
    global opposition
    global charcommand

    availablecommands = "(A)ttack, (D)efend, (S)kills, (U)pdate list"

    if char.char_class == "Knight":
        availablecommands += ", (C)harge, Cleave, Hunt"

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
        availableskills = f"{char.name} knows:\n"
        if "grun" in char.slist:
            availableskills += " GRUN (target multiple creatures)\n"

        availableskills += " LAG (weak damage)\n"
        if "comas" in char.slist:
            availableskills += " COMAS (moderate damage)\n"
        if "pas" in char.slist:
            availableskills += " PAS (fire)\n"
        if "yab" in char.slist:
            availableskills += " YAB (thunder)\n"
        if "gaa" in char.slist:
            availableskills += " GAA (earth)\n"
        if "igg" in char.slist:
            availableskills += " IGG (death)\n"
        
        
        if "leas" in char.slist:
            availableskills += " LEAS (healing)\n"
            availableskills += " TIN (weak restoration)\n"
        if "cruai" in char.slist:
            availableskills += " CRUAI (moderate restoration)\n"

        print (availableskills)
        
# PHYS SKILLS

    elif charcommand == "charge" or charcommand == "c":
        if char.char_class == "Knight" and char.hp > round(char.maxhp*0.15):
            chartarget = targetenemy()

            if chartarget is not None:

                char.hp -= round(char.maxhp*0.15)
                attacktimes = random.randint(1,3)

                for _ in range (1,attacktimes+1):

                    attackfunc(char,chartarget)

                    if chartarget.hp <= 0:
                        break

                char.acted = True
        
        else:
            print (f"{char.name} can't use this skill.")

    elif charcommand == "cleave" or charcommand == "f":
        if char.char_class == "Knight" and char.hp > round(char.maxhp*0.25):
            
            attacktimes = random.randint(1,5)
            char.hp -= round(char.maxhp*0.25)

            for _ in range(attacktimes):
                if opposition:
                    chartarget = random.choice(opposition)
                    attackfunc(char,chartarget)

                    char.acted = True
                
        else:
            print (f"{char.name} can't use this skill.")

    elif charcommand == "hunt":
        if char.char_class == "Knight" and char.hp > round(char.maxhp*0.15) and char.fp >= 3:
            chartarget = targetenemy()

            if chartarget is not None:

                char.hp -= round(char.maxhp*0.15)
                char.fp -= 3

                char.str += 3
                char.lck += 20
                attackfunc(char,chartarget)
                char.str -= 3
                char.lck -= 20

                char.acted = True
        
        else:
            print (f"{char.name} can't use this skill.")

    elif charcommand == "sneak":
        if char.char_class == "Scout" and char.fp >= 3:
            chartarget = targetenemy()

            if chartarget is not None:

                char.fp -= 3

                char.dmg += 1
                char.lck += 10
                attackfunc(char,chartarget)
                char.dmg -= 1
                char.lck -= 10

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

    elif "update" in charcommand or "u" in charcommand:
        # print ("Updating Opposition list")
        # print ("Opposition") #spacer
        # for n in opposition:
        #     print (f"({opposition.index(n)}) {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")
        # print ("") #spacer
        updatecombatlist()

    elif "rush" in charcommand:
        rushcount = int(input("How many turns to rush? (0 to cancel) "))

    elif "die" in charcommand:
        char.hp = 0
        print(f"{char.name} feel dead.")
        char.acted = True

    else:
        print("Invalid command.")

def usefp(char,fp):
    if char.fp < fp:
        print(f"{char.name} doesn't have enough FP.")
        cancast = False
    else:
        char.fp -= fp
        cancast = True
    return cancast

def calcspelldamage(char,spelllevel):
    global spelldamage
    spelldamage = 0
    if spelllevel == "weak":
        for _ in range(char.tec):
            spelldamage += random.randint(2,4)
    elif spelllevel == "medium":
        for _ in range(char.tec):
            spelldamage += random.randint(4,8)
    elif spelllevel == "heavy":
        for _ in range(char.tec):
            spelldamage += random.randint(6,12)

def calcspellheal(char,spelllevel):
    spellheal = 0
    if spelllevel == "weak":
        spellheal = 25 + char.tec//2
    elif spelllevel == "medium":
        spellheal = 50 + char.tec
    elif spelllevel == "heavy":
        spellheal = 100

    return spellheal

def spellversion(char,spell,dmgtype):
    starget = None
    if "lag" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usefp(char,10) == True:
                calcspelldamage(char,"weak")
                usespell(char,starget,dmgtype,"multi")

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usefp(char,4) == True:
                starget = targetenemy()
                if starget is not None:
                    calcspelldamage(char,"weak")
                    usespell(char,starget,dmgtype,"single")
        pass

    elif "comas" in spell and "comas" in char.slist:
        if "grun" in spell and "grun" in char.slist:
            if usefp(char,16) == True:
                calcspelldamage(char,"medium")
                usespell(char,starget,dmgtype,"multi")

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usefp(char,8) == True:
                starget = targetenemy()
                if starget is not None:
                    calcspelldamage(char,"medium")
                    usespell(char,starget,dmgtype,"single")

        pass

    elif "asmatha" in spell and "asmatha" in char.slist:
        if "grun" in spell and "grun" in char.slist:
            if usefp(char,22) == True:
                calcspelldamage(char,"heavy")
                usespell(char,starget,dmgtype,"multi")

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usefp(char,12) == True:
                starget = targetenemy()
                if starget is not None:
                    calcspelldamage(char,"heavy")
                    usespell(char,starget,dmgtype,"single")

        #cast hvy
        pass

    elif "tin" in spell and not "igg" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usefp(char,7) == True:
                heal = calcspellheal(char,"weak")
                for n in party:
                    # healally function
                    healally(char,n,heal)

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usefp(char,3) == True:
                starget = targetally()
                if starget is not None:
                    heal = calcspellheal(char,"weak")
                    healally(char,starget,heal)
        pass

    elif "cruai" in spell and "cruai" in char.slist and not "igg" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usefp(char,12) == True:
                heal = calcspellheal(char,"medium")
                for n in party:
                    # healally function
                    healally(char,n,heal)

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usefp(char,7) == True:
                starget = targetally()
                if starget is not None:
                    heal = calcspellheal(char,"medium")
                    healally(char,starget,heal)
        pass

    elif "fallain" in spell and "fallain" in char.slist and not "igg" in spell:
        if "grun" in spell and "grun" in char.slist:
            if usefp(char,30) == True:
                heal = calcspellheal(char,"heavy")
                for n in party:
                    # healally function
                    healally(char,n,heal)

        elif "grun" in spell and "grun" not in char.slist:
            print(f"{char.name} can't use this skill.")

        else:
            if usefp(char,18) == True:
                starget = targetally()
                if starget is not None:
                    heal = calcspellheal(char,"heavy")
                    healally(char,starget,heal)
        pass

    elif "igg" in spell and "tin" in spell:
        if "igg" in char.slist:
            
            if usefp(char,7) == True:
                starget = targetdeadally()
                if starget is not None:
                    starget.hp += round((starget.maxhp*30/100))

                    print (f"{starget.name} has been revived with {round(starget.maxhp*30/100)} HP!")
                    char.acted = True

    elif "igg" in spell and "cruai" in spell:
        if "igg" in char.slist and "cruai" in char.slist:

            if usefp(char,10) == True:
                starget = targetdeadally()
                if starget is not None:
                    starget.hp += round((starget.maxhp*60/100))

                    print (f"{starget.name} has been revived with {round(starget.maxhp*60/100)} HP!")
                    char.acted = True

    elif "igg" in spell and "fallain" in spell:
        if "igg" in char.slist and "fallain" in char.slist:
            if usefp(char,18) == True:
                starget = targetdeadally()
                if starget is not None:
                    starget.hp += round((starget.maxhp))

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
        print (f"({party.index(n)}) {n.name}'s HP: {n.hp}/{n.maxhp} /// FP: {n.fp}/{n.maxfp}")
    print ("") #spacer
    print ("Opposition") #spacer
    for n in opposition:
        print (f"({opposition.index(n)}) {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")
    print ("") #spacer
    initnames = ", ".join(str(n.name) for n in initiative)
    print (f"Turn order: {initnames}")


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

    # Use FP and roll damage
    # char.fp -= fpcost
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
            
            elif starget in party:
                print (f"{char.name} downed {starget.name}!")

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
    spelldamage = abs(round(spelldamage * ((math.sqrt(starget.tec)/10-1))))

    # LCK to evade spell
    sd100 = random.randint(1,100)
    
    if sd100 <= math.sqrt(starget.lck)/100:
        print (f"{starget.name} managed to avoid the attack!")

    else:
        if dmgtype in starget.weak:
            print (f"{starget.name} is weak to {dmgtype} and suffered {spelldamage*2} {dmgtype} damage!")
            spelldamage = round(spelldamage * (1.5 + math.sqrt(char.tec)))
        else:
            print (f"{starget.name} suffered {spelldamage} {dmgtype} damage.")
        starget.hp -= spelldamage

def gameover(party):
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
    global party_money

    aliveparty = 0
    for n in party:
        if n.hp >0:
            aliveparty += 1
    
    # combat_exp = round(combat_exp // aliveparty)

    for n in party:
        if n.hp >0:
            n.exp += combat_exp
    
    party_money += combat_money

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
                n.name += f" {ids[name_count]}"
            if name_count > 0:
                n.name += f" {ids[name_count]}"

    # for n in initlist:
    #     uniqueidindex = 0
    #     if initiative.count(char) > 1:
    #         for char in initiative:
    #             char.name += f" {ids[uniqueidindex]}"
    #             uniqueidindex += 1
    
    return initlist

def randomenemies():
    global opposition

    # 2d3 enemies
    number_of_enemies = random.randint(2,6)

    for _ in range(1,number_of_enemies+1):
        opposition.append(copy.deepcopy(random.choice(enemies_1)))

    # renamedopposition = renameduplicates(opposition)

    # opposition = renamedopposition

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
            enemy.fp -= 4
        elif enemy.level < 10 :
            spelllevel = "medium"
            enemy.fp -= 7
        

        if enemy.fp < 0:
            print (f"{enemy.name} tried to use a technique, but couldn't focus.")
            attackfunc(enemy,enemytarget)
        else:
            dmgtype = elem[random.randint(1,6)]

            calcspelldamage(enemy,spelllevel)
            usespell(enemy,enemytarget,dmgtype,"single")

    elif choice == "aoeelem":
    
        if enemy.level < 5:
            spelllevel = "weak"
            enemy.fp -= 4
        elif enemy.level < 10 :
            spelllevel = "medium"
            enemy.fp -= 7

        if enemy.fp < 0:
            print (f"{enemy.name} tried to use a technique, but couldn't focus.")
            attackfunc(enemy,enemytarget)
        else:
            dmgtype = elem[random.randint(1,6)]

            calcspelldamage(enemy,spelllevel)
            usespell(enemy,enemytarget,dmgtype,"multi")


    pass


plevel_exp = [0,500,1000,1500,2000,5000,12000]

def checkPLevel(char):

    # if char.exp >= plevel_exp[char.plevel]:
    if char.exp >= char.plevel*1000:
        os.system("cls")
        print(f"{char.name} has leveled up!")
        levelUpChar(char)

def pickClass(cname):
    for n in cclasses:
        if n.name == cname:
            return n

def levelUpChar(char):
    class_choice = pickClass(char.char_class)
    choice_made = False
    char.plevel += 1
    
    while choice_made == False:
    
        choice = input(f"What do you want to improve?\n Max (H)P: {char.maxhp} >>> {char.maxhp+class_choice.hp}\n Max (F)P: {char.maxfp} >>> {char.maxfp+class_choice.fp}\n (T)ec: {char.tec} >>> {char.tec+1}\n (S)pd: {char.agi} >>> {char.agi+1}\n (L)ck: {char.lck} >>> {char.lck+1}\n\n")

        if choice.lower() == "h":
            final_choice = input(f"\nThis will increase your Max HP by {class_choice.hp}.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.maxhp += class_choice.hp
                char.hp += class_choice.hp
                choice_made = True

            if final_choice.lower() == "n":
                pass
    
        elif choice.lower() == "f":
            final_choice = input(f"\nThis will increase your Max FP by {class_choice.fp}.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.maxfp += class_choice.fp
                char.maxfp += class_choice.fp
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "t":
            final_choice = input(f"\nThis will increase your Tec by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.tec += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "s":
            final_choice = input(f"\nThis will increase your agi by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.agi += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "l":
            final_choice = input(f"\nThis will increase your Lck by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.lck += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass




        
# GAME
def runCombat():
    global combat_money
    global combat_exp
    global rounds

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
                checkPLevel(n)
            
            return
            # break

        rounds += 1
        print (f"Round {rounds}")
        print ("") #spacer
        print ("Party:") #spacer
        for n in party:
            print (f"({party.index(n)}) {n.name}'s HP: {n.hp}/{n.maxhp} /// FP: {n.fp}/{n.maxfp}")
        print ("") #spacer
        print ("Opposition") #spacer
        for n in opposition:
            print (f"({opposition.index(n)}) {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")
        print ("") #spacer

        initnames = ", ".join(str(n.name) for n in initiative)
        print (f"Turn order: {initnames}")
        
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
                time.sleep(0.4)
            
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
                    time.sleep(0.4)

        if gameover(party):
            print ("")
            print ("Game Over.")
            break

        endofturncleanup()

        input("Type anything to continue: ")


# TESTING
# runCombat()


# Create PHYS skills for non-casters (buffs, defense, physical attacks)
    # Multi-hit variant for all enemies
    # Medium/Heavy damage variants
    # High crit rate attack