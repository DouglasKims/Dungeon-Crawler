# create dice rolling functions
# create a turn based combat system

import os
import time
import random

class Character:
    def __init__(self,name,cclass,maxhp,hp,maxfp,fp,atk,tec,dfn,spd,lck,slist,acted,defending,weak):
        self.name = name
        self.cclass = cclass
        self.maxhp = maxhp
        self.hp = hp
        self.maxfp = maxfp
        self.fp = fp
        self.atk = atk
        self.tec = tec
        self.dfn = dfn
        self.spd = spd
        self.lck = lck
        self.slist = slist
        self.acted = acted
        self.defending = defending
        self.weak = weak

class Enemy:
    def __init__(self,name,maxhp,hp,atk,dfn,spd,lck,defending,weak):
        self.name = name
        self.maxhp = maxhp
        self.hp = hp
        self.atk = atk
        self.dfn = dfn
        self.spd = spd
        self.lck = lck
        self.defending = defending
        self.weak = weak

h1spells = ["dia","media","maragi","agi"]
h2spells = ["dia","garu"]

""" 0: Phys
    1: fire
    2: wind
    3: earth
    4: ice
    5: thunder
    6: toxin
"""

elements = ["phys","fire","wind","earth","ice","thunder","toxin"]

hero1 = Character("Deaughe","Bard",40,40,30,30,4,8,0,5,5,h1spells,False,False,[])
hero2 = Character("Duncan","Tank",60,60,10,10,6,3,0,3,3,h2spells,False,False,[])
enemy1 = Enemy("Thug",60,60,5,2,0,0,False,[elements[1],elements[2]])
enemy2 = Enemy("Bandit",40,40,5,0,5,0,False,[elements[0],elements[2]])
party = [hero1,hero2]
opposition = [enemy1,enemy2]

atkmod = 0
d100 = 0
dmgdice = 0
damage = 0
finaldamage = 0
enemytarget = None
chartarget = None
charcommand = None

def rollattack(char):
    global atkmod
    global d100
    d100 = random.randint(1,100)

    if d100 >= 96:
        print("Miss!")
        atkmod = -100
    elif d100 >= 80+char.lck:
            print("Fumble!")
            atkmod = -10
    else:
        if d100 <= char.lck:
            print("Critical Hit!")
            atkmod = 10
        else:
            atkmod = 0

    return atkmod

def rolldamage(char):
    rolleddamage = 0
    for _ in range(char.atk):
        rolleddamage += random.randint(1,5)
    return rolleddamage

def attackfunc(attacker,target):
    global finaldamage

    rollattack(attacker)

    finaldamage = atkmod + rolldamage(attacker) - target.dfn
    
    if finaldamage > 0:
        if "phys" in target.weak:
            finaldamage * 2
            print (f"{attacker.name} attacks {target.name}, who's weak to Physical attacks for {finaldamage} damage!")

        elif target.defending == True:
            finaldamage // 2
            print (f"{n.name} attacks {enemytarget.name}, but they defended and suffered only {finaldamage} damage.")

        else:
            print (f"{attacker.name} attacks {target.name} for {finaldamage} damage.")

        target.hp -= finaldamage

    elif finaldamage <= 0:
        print (f"{attacker.name} attacks {target.name}, but causes no damage.")

    if target.hp <= 0 and target in opposition:
        opposition.remove(target)
        print (f"{attacker.name} defeated {target.name}!")

def command(char):
    global chartarget
    global opposition
    global finaldamage
    global charcommand

    charcommand = input(f"What is {char.name} doing? ")
    
    if charcommand == "attack":

        chartarget = targetenemy()

        attackfunc(char,chartarget)
        
        char.acted = True
        pass
    
    elif charcommand == "media":
        if char.fp <10:
            print(f"{char.name} doesn't have enough FP.")
        else:
            char.fp -= 10
            spelldamage = 0
            for _ in range(char.tec//2):
                spelldamage += random.randint(1,6)
            spelldamage += 10
            for n in party:
                print (f"{n.name} has been healed for {spelldamage}")
                n.hp += spelldamage

                if n.hp > n.maxhp:
                    n.hp = n.maxhp

            char.acted = True
        pass

    elif charcommand == "dia":
        if "dia" not in char.slist:
            print(f"{char.name} can't cast Dia.")
            pass
        if char.fp <4:
            print(f"{char.name} doesn't have enough FP.")
        else:
            char.fp -= 4
            spelldamage = 0
            for _ in range(char.tec//2):
                spelldamage += random.randint(1,6)
            spelldamage += 10
            
            starget = targetally()

            print (f"{starget.name} has been healed for {spelldamage}")
            starget.hp += spelldamage

            if starget.hp > starget.maxhp:
                starget.hp = starget.maxhp

            char.acted = True
        pass

    elif charcommand == "maragi":
        if "maragi" not in char.slist:
            print(f"{char.name} can't cast Maragi.")
            pass
        else:
            if char.fp <15:
                print(f"{char.name} doesn't have enough FP.")
            else:
                usespell(char,None,"fire",15,"multi")

            char.acted = True
        pass

    elif charcommand == "agi":
        if "agi" not in char.slist:
            print(f"{char.name} can't cast Agi.")
            pass
        else:
            if char.fp <6:
                print(f"{char.name} doesn't have enough FP.")
            else:
                starget = targetenemy()

                usespell(char,starget,"fire",6,"single")

            char.acted = True
        pass

    elif charcommand == "garu":
        if "garu" not in char.slist:
            print(f"{char.name} can't cast Garu.")
            pass
        else:
            if char.fp <6:
                print(f"{char.name} doesn't have enough FP.")
            else:
                starget = targetenemy()
                
                usespell(char,starget,"wind",6,"single")

            char.acted = True
        pass

    elif charcommand == "defend":
        char.defending = True
        print (f"{char.name} is defending.")

        char.acted = True
        pass

## Logic

def targetenemy():
    stargetindex = None
    while stargetindex == None:
        stargetindex = int(input("Who are you targeting? "))
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
        stargetindex = int(input("Who are you targeting? "))
        if stargetindex in range(0,len(party)):
            starget = party[int(stargetindex)]
        else:
            print("Invalid target.")
            stargetindex = None
    target = starget
    return target

def usespell(char,starget,dmgtype,fpcost,spelltype):
    global spelldamage
    defeatedopp = []

    # Use FP and roll damage
    char.fp -= fpcost
    spelldamage = 0
    for _ in range(char.tec):
        spelldamage += random.randint(1,6)

    if spelltype == "single":
        dealspelldamage(starget,dmgtype,spelldamage)
        if starget.hp <= 0:
            opposition.remove(starget)
            print (f"{char.name} defeated {starget.name}!")
    elif spelltype == "multi":
        for n in opposition:
            dealspelldamage(n,dmgtype,spelldamage)
            if n.hp <= 0:
                defeatedopp.append(n)
                
        for n in defeatedopp:
            print (f"{char.name} defeated {n.name}!")
            opposition.remove(n)
            pass

def dealspelldamage(starget,dmgtype,spelldamage):
    if dmgtype in starget.weak:
        print (f"{starget.name} is weak to {dmgtype} and suffered {spelldamage*2} {dmgtype} damage!")
        spelldamage = spelldamage * 2
    else:
        print (f"{starget.name} suffered {spelldamage} {dmgtype} damage.")
    starget.hp -= spelldamage
    

## Game
rounds = 0

## initiative system
initvalue = {}
for n in party:
    initvalue.update({n:random.randint(1,10)+n.spd})
for n in opposition:
    initvalue.update({n:random.randint(1,10)+n.spd})

initiative = sorted(initvalue.items(),key=lambda x:x[1], reverse=True)
initturn = 0

testing = True
while testing:

    os.system('cls')

    if not opposition:
        testing = False
        print(f"You win the combat in {rounds} rounds!")
        break

    rounds += 1
    print (f"Round {rounds}")
    
    for n in party:
        print (f"({party.index(n)}) {n.name}'s HP: {n.hp}/{n.maxhp} /// FP: {n.fp}/{n.maxfp}")    
    for n in opposition:
        print (f"({opposition.index(n)}) {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")

    print ("")
    print(initiative)
    print (f"{initiative[initturn.name]}'s turn")

    for n in party:
        n.acted = False
        n.defending = False
        if not opposition:
            pass
        else:
            while n.acted == False:
                command(n)

            print ("")
            time.sleep(0.4)

    if not opposition:
        pass
    else:
        for n in opposition:
            enemytarget = random.choice(party)
            attackfunc(n,enemytarget)

            print ("")
            time.sleep(0.4)

    input("Type anything to continue: ")

    