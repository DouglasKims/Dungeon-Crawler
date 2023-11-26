# create dice rolling functions
# create a turn based combat system

from math import e
import os
import time
import random
import copy

class Character:
    def __init__(self,name,char_class,level,plevel,maxhp,hp,maxfp,fp,atk,dmg,tec,dfn,spd,lck,slist,acted,defending,weak,equip,exp,init):
        self.name = name
        self.char_class = char_class
        self.level = level
        self.plevel = plevel
        self.maxhp = maxhp
        self.hp = hp
        self.maxfp = maxfp
        self.fp = fp
        self.atk = atk
        self.dmg = dmg
        self.tec = tec
        self.dfn = dfn
        self.spd = spd
        self.lck = lck
        self.slist = slist
        self.acted = acted
        self.defending = defending
        self.weak = weak
        self.equip = equip
        self.exp = exp
        self.init = init

class Enemy:
    def __init__(self,name,level,maxhp,hp,atk,dmg,dfn,spd,lck,defending,weak,exp,money,init):
        self.name = name
        self.level = level
        self.maxhp = maxhp
        self.hp = hp
        self.atk = atk
        self.dmg = dmg
        self.dfn = dfn
        self.spd = spd
        self.lck = lck
        self.defending = defending
        self.weak = weak
        self.exp = exp
        self.money = money
        self.init = init

class CClass:
    def __init__(self,name,hp,fp,fpinc,atk,dmg,tec,dfn,spd,lck,special):
        self.name = name
        self.hp = hp
        self.fp = fp
        self.fpinc = fpinc
        self.atk = atk
        self.dmg = dmg
        self.tec = tec
        self.dfn = dfn
        self.spd = spd
        self.lck = lck
        self.special = special

# Character Classes
warrior = CClass("Warrior",10,20,3,6,1,3,4,3,3,None)
druid = CClass("Druid",8,50,6,6,1,8,2,3,3,None)
bard = CClass("Bard",8,40,5,6,1,6,2,5,6,None)

cclasses = [warrior,druid,bard]

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
dan = Character("Thorudan","Druid",1,1,80,80,50,50,4,1,10,2,3,3,danspells,False,False,[],dan_equip,0,0)
mars = Character("Mars","Warrior",1,1,100,100,20,20,8,2,3,4,3,3,marsspells,False,False,[],mars_equip,0,0)

enemy1 = Enemy("Evil Soul",1,60,60,5,1,2,0,0,False,[elem[1],elem[2]],5,5,0)
enemy2 = Enemy("Malignant Spirit",2,40,40,5,1,0,5,0,False,[elem[0],elem[2]],10,10,0)
enemy3 = Enemy("Despicable Shade",3,30,30,4,1,2,6,0,False,[elem[1],elem[3]],15,20,0)
enemy4 = Enemy("Troublesome Ghost",1,80,80,5,1,3,2,0,False,[elem[1],elem[2],elem[3],elem[4],elem[5],elem[6]],5,5,0)

enemies_1 = [enemy1,enemy2,enemy3,enemy4]

party = [drav,dan,mars]
party_money = 0
opposition = []

atkmod = 0
d100 = 0
dmgdice = 0
damage = 0
enemytarget = None
chartarget = None
charcommand = None
rounds = 0



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
        if char.dmg == 1:
            rolleddamage += random.randint(1,4)
        elif char.dmg == 2:
            rolleddamage += random.randint(2,6)
        elif char.dmg == 3:
            rolleddamage += random.randint(3,8)
        elif char.dmg >= 4:
            rolleddamage += random.randint(4,10)

    rolleddamage = rolleddamage * char.level + char.atk
    return rolleddamage

def attackfunc(attacker,target):
    global opptoremove

    rollattack(attacker)

    finaldamage = atkmod + rolldamage(attacker) - ( target.dfn * target.level)
    
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

    availablecommands = "(A)ttack, (D)efend, (S)kills"

    if char.char_class == "Warrior":
        availablecommands += ", (C)harge"

    availablecommands += ", (or type a combination of skills to use them)"

    charcommand = input(f"What is {char.name} doing?\n {availablecommands}\n").lower()

    if charcommand == "attack" or charcommand == "a":

        chartarget = targetenemy()

        if chartarget is not None:

            attackfunc(char,chartarget)
            
            char.acted = True

            
        pass
    
    elif charcommand == "charge" or charcommand == "c":
        if char.char_class == "Warrior":
            chartarget = targetenemy()

            if chartarget is not None:

                char.hp -= round(char.maxhp*0.15)
                attacktimes = random.randint(1,3)

                for _ in range (1,attacktimes+1):

                    attackfunc(char,chartarget)

                    if chartarget.hp <= 0:
                        break

                char.acted = True

    elif charcommand == "defend" or charcommand == "d":
        char.defending = True
        print (f"{char.name} is defending.")

        char.acted = True
        pass

    elif charcommand == "skill" or charcommand == "skills" or charcommand == "s":
        availableskills = f"{char.name} knows"
        if "grun" in char.slist:
            availableskills += ", GRUN (target multiple creatures)"

        availableskills += ", LAG (weak damage)"
        if "comas" in char.slist:
            availableskills += ", COMAS (moderate damage)"
        if "pas" in char.slist:
            availableskills += ", PAS (fire)"
        if "yab" in char.slist:
            availableskills += ", YAB (thunder)"
        if "gaa" in char.slist:
            availableskills += ", GAA (earth)"
        if "igg" in char.slist:
            availableskills += ", IGG (death)"
        
        
        if "leas" in char.slist:
            availableskills += ", LEAS (healing)"
            availableskills += ", TIN (weak restoration)"    
        if "cruai" in char.slist:
            availableskills += ", CRUAI (moderate restoration)"

        print (availableskills)
        
            

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

    elif "update" in charcommand:
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
                starget = targetally()
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
                starget = targetally()
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
                starget = targetally()
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
        
        if stargetindex in cancelterms:
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

        if stargetindex in cancelterms:
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

        if stargetindex in cancelterms:
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

    # Use FP and roll damage
    # char.fp -= fpcost
    # spelldamage = 0
    # for _ in range(char.tec):
    #     spelldamage += random.randint(1,6)

    if spelltype == "single":
        dealspelldamage(starget,dmgtype,spelldamage)
        if starget.hp <= 0:
            opposition.remove(starget)
            opptoremove.append(starget)
            print (f"{char.name} defeated {starget.name}!")
    elif spelltype == "multi":
        for n in opposition:
            dealspelldamage(n,dmgtype,spelldamage)
            if n.hp <= 0:
                defeatedopp.append(n)

        print("")
        for n in defeatedopp:
            print (f"{char.name} defeated {n.name}!")
            opposition.remove(n)
            opptoremove.append(n)
            pass
    
    char.acted = True

def dealspelldamage(starget,dmgtype,spelldamage):
    if dmgtype in starget.weak:
        print (f"{starget.name} is weak to {dmgtype} and suffered {spelldamage*2} {dmgtype} damage!")
        spelldamage = spelldamage * 2
    else:
        print (f"{starget.name} suffered {spelldamage} {dmgtype} damage.")
    starget.hp -= spelldamage

def gameover(party):
    return all(n.hp == 0 for n in party)

opptoremove = []
combat_money = 0
combat_exp = 0

def endofturncleanup():
    global initiative
    global opptoremove
    global combat_exp
    global combat_money

    for n in opptoremove:
        combat_exp += n.exp
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
    
    combat_exp = round(combat_exp // aliveparty)

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
        initroll = random.randint(1,10)+n.spd
        initdict.update({n: initroll})
    for n in opposition:
        initroll = random.randint(1,10)+n.spd
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

plevel_exp = [0,50,200,500,1500,5000,12000]

def checkPLevel(char):

    if char.exp >= plevel_exp[char.plevel]:
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
    
        choice = input(f"What do you want to improve?\n Max (H)P: {char.maxhp} >>> {char.maxhp+class_choice.hp}\n Max (F)P: {char.maxfp} >>> {char.maxfp+class_choice.fpinc}\n (T)ec: {char.tec} >>> {char.tec+1}\n (S)pd: {char.spd} >>> {char.spd+1}\n (L)ck: {char.lck} >>> {char.lck+1}\n\n")

        if choice.lower() == "h":
            final_choice = input(f"\nThis will increase your Max HP by {class_choice.hp}.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.maxhp += class_choice.hp
                char.hp += class_choice.hp
                choice_made = True

            if final_choice.lower() == "n":
                pass
    
        elif choice.lower() == "f":
            final_choice = input(f"\nThis will increase your Max FP by {class_choice.fpinc}.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.maxfp += class_choice.fpinc
                char.maxfp += class_choice.fpinc
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
            final_choice = input(f"\nThis will increase your Spd by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y":
                char.spd += 1
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
            print(f"You won the combat in {rounds} rounds!\nThe party gains {combat_money} and each party member receives {combat_exp} experience.")
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
                enemytarget = None
                while enemytarget == None or enemytarget.hp == 0:
                    enemytarget = random.choice(party)
                attackfunc(n,enemytarget)

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

# randomenemies()
# rollinitiative()
# initnames = ", ".join(str(n.name) for n in initiative)
# print (f"Turn order: {initnames}")
# rounds = 0

# testing = True
# while testing:

#     os.system('cls')

#     if not opposition:
#         testing = False
#         print(f"You won the combat in {rounds} rounds!")
#         break

#     rounds += 1
#     print (f"Round {rounds}")
#     print ("") #spacer
#     print ("Party:") #spacer
#     for n in party:
#         print (f"({party.index(n)}) {n.name}'s HP: {n.hp}/{n.maxhp} /// FP: {n.fp}/{n.maxfp}")
#     print ("") #spacer
#     print ("Opposition") #spacer
#     for n in opposition:
#         print (f"({opposition.index(n)}) {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")
#     print ("") #spacer

#     initnames = ", ".join(str(n.name) for n in initiative)
#     print (f"Turn order: {initnames}")
    
#     print ("") #spacer

#     for n in initiative:
#         if n not in party and n.hp <= 0:
#             pass
#         else:
#             print(f"It's {n.name}'s turn!")
#         if n in party and n.hp <= 0:
#             print (f"But they're down.")
#             print ("")

#         if n in opposition and n.hp > 0:
#             enemytarget = None
#             while enemytarget == None or enemytarget.hp == 0:
#                 enemytarget = random.choice(party)
#             attackfunc(n,enemytarget)

#             #game over function
#             if gameover(party):
#                 print ("")
#                 print ("All heroes have been defeated.")
#                 break

#             print ("")
#             time.sleep(0.4)
        
#         elif n in party:
#             n.acted = False
#             n.defending = False
#             if not opposition:
#                 pass
#             elif n.hp <= 0:
#                 pass
#             else:
#                 while n.acted == False:
#                     command(n)

#                 print ("")
#                 time.sleep(0.4)

#     if gameover(party):
#         print ("")
#         print ("Game Over.")
#         break

#     endofturncleanup()

#     input("Type anything to continue: ")


# Create PHYS skills for non-casters (buffs, defense, physical attacks)
    # Multi-hit variant for all enemies
    # Medium/Heavy damage variants
    # High crit rate attack

# Create equipment system
    # equipping and unequipping equipment (shouldn't be done in combat)
    # equip. should increase heroes' ATK, DEF, (maybe change weak/resist)

# Create Perks system
    # defeating enemies grant EXP, each EXP*perks+1 reached gives a new perk.
    # Perks can increase > base HP, FP, SPD, LCK, TEC
    # SPD/LCK/TEC can't be higher than 15
    # HP increases are based on class / 10% of class' max
    # FP increases are based on class / 10% of class' max
    # Every 10(?) perks, characters get access to new spell level/type


# mu/fire > mu/fireza > mu/firezaon
# mul/ice > mul/iceza > mul/icezaon
# mul/air > mul/airza > mul/airzaon
# mu/rock > mu/rockza > mu/rockzaon
# mu/zap > mu/zapza > mu/zapzaon
# mu/tox > mu/toxza > mu/toxzaon

# fire / fire-sta / fire-sta-za
# fire-mor (big) / fire-mortha (biggest)

# cure / curemor / curemortha
# revive / revivemor

# haste / slow
# shield / barrier

# Almighty        buff / debuff / damage / Heal
# yabarag         atk + / atk - / thunder / rage-
# haka pf'hagan   haste / slow / decay / regen
# igglebeth       resist death + / kill / toxic / revive
# irgh d'ebram    mdef + / mdef -/ ice / poison-
# famphegor       reflect / sleep / air / confuse -
# gaaphadur       pdef + / pdef - / earth / condition -
# pasperon        lck + / lck- / fire / heal
# khosme          - / - / chaos / 

# Grun > Several targets
# Lag > weak damage / negative (weak / lag)
# Comas > medium damage / negative (capable / comasach)
# Asmatha > heavy damage / negative (biggest/motha)
# Tin > weak heal / positive (ill / tinn)
# Cruai > medium heal / positive (tough / cruaidh)
# Fallain > heavy heal / positive (fallain / healthy)
# Leas > buff (improve / leasaich)
# Mios > debuff (worse / nas miosa)

# fire > Grun/Pas/mor // /Pas/matha
# water > Grun/Irg/mor // Irg/matha
# earth > Grun/Gaa/mor // Gaa/matha
# air > Grun/Fam/mor // Fam/matha