import math
import os
import copy
import CombatSystem


# LOGIC

class Equipment():
    def __init__(self,name,type,level,special,str,dmg,vit,weak,resist, value):
        self.name = name
        self.type = type
        self.level = level
        self.special = special
        self.str = str
        self.dmg = dmg
        self.vit = vit
        self.weak = weak
        self.resist = resist
        self.value = value

class Consumable():
    def __init__(self, name, type, effect, value):
        self.name = name
        self.type = type
        self.effect = effect
        self.value = value

# Equip types: Armor, Weapon, Accessory

armor1 = Equipment("Leather Armor","Armor",1,None,0,0,1,None,None,100)
armor2 = Equipment("Chain Mail","Armor",1,None,0,0,3,None,None,250)
weapon1 = Equipment("Battle Axe","Weapon",1,None,1,1,0,None,None,100)
weapon2 = Equipment("Vicious Blade","Weapon",1,None,0,2,0,None,None,500)
weapon5 = Equipment("Longsword +1","Weapon",2,"Dmg +",2,2,0,None,None,1500)
weapon6 = Equipment("Longsword +2","Weapon",3,"Dmg ++",3,3,0,None,None,5000)
access1 = Equipment("Shield","Accessory",1,None,-1,0,5,None,None,300)
access2 = Equipment("Magic Ring","Accessory",1,"tec+",0,0,1,None,None,700)

item1 = Consumable("Healing Draught","Healing","Heal 30 HP",50)
item2 = Consumable("Invigorating Tonic","Healing","Heal 15 tp",200)
item3 = Consumable("Charged Memento","Reviving","Revives with 25% HP", 200)

# EQUIPMENT
inventory = []
# inventory.append(copy.deepcopy(armor1))
# inventory.append(copy.deepcopy(armor2))
# inventory.append(copy.deepcopy(weapon1))
# inventory.append(copy.deepcopy(access1))

# CONSUMABLES
consumables = []
# for n in range(3):
#     consumables.append(copy.deepcopy(item1))
# consumables.append(copy.deepcopy(item2))
# consumables.append(copy.deepcopy(item3))

party = CombatSystem.party

def chooseCharacter():
    print("Which Character are you managing?")
    for n in party:
        print (f"({party.index(n)}) {n.name}")
    char = input()
    
    if char in cancelterms:
            print("")
            return None
    
    try:
        char = int(char)
    except ValueError:
        char = None

    

    if char in range(0,len(party)):
        char = party[char]
        return char

    elif char == None:
        print("Invalid choice")
        return None

def getEquip(char):

    print(f"{char.name}'s Equipment:")
    for slot, equipment in char.equip.items():
        if equipment is not None:
            print(f"{slot}: {equipment.name}")
        else:
            print(f"{slot}: {equipment}")

def getStatus():

    char = chooseCharacter()
    if char == None:
            print("")
            return

    print(f"{char.name}'s Status\n Class: {char.char_class.name}\n Level: {char.level} ({round(char.exp)} / {round(char.level*1000)} EXP)\n HP: {math.floor(char.hp)} / {math.floor(char.maxhp)}\n tp: {math.floor(char.tp)} / {math.floor(char.maxtp)}\n STR: {math.floor(char.str)} (DMG: {char.dmg})\n TEC: {math.floor(char.tec)}\n VIT: {math.floor(char.vit)}\n AGI: {math.floor(char.agi)}\n LCK: {math.floor(char.lck)}\n")
    # getEquip func
    getEquip(char)

def getSkills():
    char = chooseCharacter()
    if char == None:
            print("")
            return
    availableskills = ""

    if char.char_class.name == "Knight":
        availableskills += f"{char.name} knows these STR-based skills:\n"
        availableskills += "    CHARGE: Attacks one opponent up to three times (costs 15% HP)\n"
        availableskills += "    HUNT: Attacks one opponent with increased strenght and crit chance (costs 15% HP and 3 TP)\n"
        availableskills += "    CLEAVE: Attacks random opponents up to five times (costs 25% HP)\n"
        availableskills += "\n"
    
    if char.char_class.name == "Scout":
        availableskills += f"{char.name} knows these SCOUT skills:\n"
        availableskills += "    SNEAK: Attacks one opponent with increased damage and crit chance (costs 3 TP)\n"
        availableskills += "    HIDE: Lower odds of being targeted for remainder of fight (costs 3 TP)\n"

    availableskills += f"{char.name} knows these TEC-based skills:\n"
    if "grun" in char.slist:
        availableskills += "    GRUN: Target multiple creatures(ally or opponents)\n"

    availableskills += "    LAG: Causes Light amount of damage (4tp, 10tp if used with Grun)\n"
    if "comas" in char.slist:
        availableskills += "    COMAS: Causes moderate amount of damage (8tp, 16tp if used with Grun)\n"
    if "pas" in char.slist:
        availableskills += "    PAS: Blessings of Pasperon commands FIRE.\n"
    if "yab" in char.slist:
        availableskills += "    YAB: Blessings of Yabarag commands THUNDER.\n"
    if "gaa" in char.slist:
        availableskills += "    GAA: Blessings of Gaaphadur commands EARTH.\n"
    if "igg" in char.slist:
        availableskills += "    IGG: Blessings of Igglebeth commands DEATH.\n"
    
    availableskills += "\n"
    availableskills += f"{char.name} knows these TEC-based Support skills:\n"
    if "leas" in char.slist:
        availableskills += "    LEAS: Heals an ally who's still alive.\n"
        availableskills += "    TIN: Weak degree of restoration (3tp, 7tp if used with Grun or Igg to revive)\n"    
    if "cruai" in char.slist:
        availableskills += "    CRUAI: Moderate degree of restoration (7tp, 12tp if used with Grun or Igg to revive)\n"

    print (availableskills)

def partyRecovery():
    tpcost = 0
    totaltp = 0
    totaltpcost = 0

    for n in party:
        if n.hp <= 0:
            tpcost += 5
            totaltp += n.tp
        elif n.hp < n.maxhp:
            tpcost += (n.hp - n.maxhp)* -1/20 + 1
            totaltp += n.tp
        else:
            totaltp += n.tp

    
    # tpcost = round(tpcost//len(CombatSystem.party))

    if totaltp >= tpcost:

        tpcost = round(tpcost//len(party))
        totaltpcost = tpcost * len(party)
        choice = input(f"This will use {totaltpcost} tp split between party member to revive fallen allies and fully heal the wounded.\nDo you want to continue? (No to cancel)\n").lower()

        if choice in cancelterms:
                print("")
                return None
        else:
            for n in party:
                    n.hp = n.maxhp
            
            while totaltpcost > 0:
                for n in party:
                    if n.tp >= tpcost:
                        if tpcost > totaltpcost:
                            totaltpcost -= tpcost
                            n.tp -= totaltpcost    
                        else:
                            totaltpcost -= tpcost
                            n.tp -= tpcost
    
    else:
        print("The party doesn't have enough tp to fully recover.")


def getInventory():

    print("Consumables:")
    for n in consumables:
        print (f"    ({consumables.index(n)}) {n.name} // Type: {n.type} // Effect: {n.effect} // Value: {n.value} Cr")

    print("\nEquipment:")
    for n in inventory:
        # print (f"    ({inventory.index(n)}) {n.name} // Type: {n.type} // STR: {n.str} (Dmg: {n.dmg}) // VIT: {n.vit} // Weak: {n.weak} // Resist: {n.resist} // Special: {n.special} // Value: {n.value} Cr")
        print (f"    ({inventory.index(n)}) {n.name} // Type: {n.type} // STR: {n.str} (Dmg: {n.dmg}) // VIT: {n.vit} // Value: {n.value} Cr")


    useitem = input(f"\nAre you using any item? If so, type the consumable number, otherwise press anything.\n")

    try:
        useitem = int(useitem)
    except ValueError:
        useitem = None

    if useitem in range(0,len(consumables)):
        print("using item")
        print("")
        useItem(consumables[useitem])
    else:
        return
    

def useItem(item):


    if item.type == "Healing":
        iname, ipower, ieffect = item.effect.split()
        ipower = int(ipower)
        
        if ieffect == "HP":

            print("Party:")
            for char in party:
                print(f"  ({party.index(char)}) {char.name} // HP: {math.floor(char.hp)} / {math.floor(char.maxhp)}")
            choice = input(f"This {item.name} will heal {ipower} HP. Who's using it?\n")

            if choice in cancelterms:
                print("")
                return None
            
            try:
                choice = int(choice)
                choice = party[choice]
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid character.")
                return None

            if choice.hp <= 0:
                print("Can't be used on dead character.")
                return

            choice.hp += ipower
            consumables.remove(item)
            print(f"{choice.name} recovered {ipower} HP.")

        elif ieffect == "TP":

            print("Party:")
            for char in party:
                print(f"  ({party.index(char)}) {char.name} // tp: {math.floor(char.tp)} / {math.floor(char.maxtp)}")
            choice = input(f"This {iname} will heal {ipower} TP. Who's using it?\n")

            if choice in cancelterms:
                print("")
                return None
            
            try:
                choice = int(choice)
                choice = party[choice]
            except (ValueError, IndexError):
                print("Invalid input. Please enter a valid character.")
                return None
            
            choice.tp += ipower
            consumables.remove(item)
            print(f"{choice.name} recovered {ipower} tp.")

    if item.type == "Reviving":
        ieffect, i1, ipower, i2 = item.effect.split()

        print("Party:")
        for char in party:
                print(f"  ({party.index(char)}) {char.name} // HP: {math.floor(char.hp)} / {math.floor(char.maxhp)}")
        choice = input(f"This {item.name} will revive with {ipower} HP. Who's using it?\n")

        if choice in cancelterms:
            print("")
            return None
        
        try:
            choice = int(choice)
            choice = party[choice]
        except (ValueError, IndexError):
            print("Invalid input. Please enter a valid character.")
            return None

        if choice.hp > 0:
            print("Can't be used on a living character.")
            return

        if ipower == "50%":
            choice.hp += round(choice.maxhp//2)
        elif ipower == "25%":
            choice.hp += round(choice.maxhp//4)

        consumables.remove(item)
        print(f"{choice.name} was revived with {ipower} HP.")

def changeEquip():
    
    char = chooseCharacter()
    if char == None:
            print("")
            return

    # ======================================
    print(f"What slot are you equiping for {char.name}\n")
    getEquip(char)
    slot = input("(W)eapon, (A)rmor, Accessory(1), or Accessory(2)?\n")

    if slot in cancelterms:
            print("")
            return None

    if slot.lower() == "w":
        
        if char.equip["Weapon"] != None:
            print(f"{char.name} already has a {char.equip['Weapon'].name} equipped. \nPlease remove equipment first.")

        else:
            list_weapon = []
            for n in inventory:
                if n.type == "Weapon":
                    list_weapon.append(n)

            if list_weapon != []:

                print (f"What Weapon will {char.name} equip?")
                for n in list_weapon:
                    print (f"({list_weapon.index(n)}) {n.name} // STR: {n.str} // Special: {n.special}")

                try:
                    wpn = int(input())
                except ValueError:
                    wpn = None

                if wpn in range(0,len(list_weapon)):
                    wpn = list_weapon[wpn]

                char.equip["Weapon"] = wpn
                inventory.remove(wpn)

                char.str += wpn.str
                char.dmg += wpn.dmg
            
            else:
                print ("No weapons to equip.")

    elif slot.lower() == "a":
        
        if char.equip["Armor"] != None:
            print(f"{char.name} already has a {char.equip['Armor'].name} equipped. \nPlease remove equipment first.")

        else:

            list_armor = []
            for n in inventory:
                if n.type == "Armor":
                    list_armor.append(n)

            if list_armor != []:

                print (f"What Armor will {char.name} equip?")
                for n in list_armor:
                    print (f"({list_armor.index(n)}) {n.name} // VIT: {n.vit} // Special: {n.special} // Weak to: {n.weak} // Resists: {n.resist}")

                try:
                    arm = int(input())
                except ValueError:
                    arm = None

                if arm in range(0,len(list_armor)):
                    arm = list_armor[arm]

                char.equip["Armor"] = arm
                inventory.remove(arm)

                char.vit += arm.vit
                # for n in arm.weak:
                #     char.weak.append(n)
            
            else:
                print ("No armor to equip.")

    elif slot.lower() == "1":
        
        if char.equip["Accessory 1"] != None:
            print(f"{char.name} already has a {char.equip['Accessory 1'].name} equipped. \nPlease remove equipment first.")

        else:

            list_acc = []
            for n in inventory:
                if n.type == "Accessory":
                    list_acc.append(n)

            if list_acc != []:

                print (f"What Accessory will {char.name} equip?")
                for n in list_acc:
                    print (f"({list_acc.index(n)}) {n.name} // STR: {n.str} // VIT: {n.vit} // Special: {n.special} // Weak to: {n.weak} // Resists: {n.resist}")

                try:
                    acc = int(input())
                except ValueError:
                    acc = None

                if acc in range(0,len(list_acc)):
                    acc = list_acc[acc]

                char.equip["Accessory 1"] = acc
                inventory.remove(acc)

                char.str += acc.str
                char.vit += acc.vit
                for n in arm.weak:
                    char.weak.append(n)
                char.dmg += wpn.dmg

            
            else:
                print ("No Accessories to equip.")

    elif slot.lower() == "2":
        
        if char.equip["Accessory 2"] != None:
            print(f"{char.name} already has a {char.equip['Accessory 2'].name} equipped. \nPlease remove equipment first.")

        list_acc = []
        for n in inventory:
            if n.type == "Accessory":
                list_acc.append(n)

        if list_acc != []:

            print (f"What Accessory will {char.name} equip?")
            for n in list_acc:
                print (f"({list_acc.index(n)}) {n.name} // STR: {n.str} // VIT: {n.vit} // Special: {n.special} // Weak to: {n.weak} // Resists: {n.resist}")

            try:
                acc = int(input())
            except ValueError:
                acc = None

            if acc in range(0,len(list_acc)):
                acc = list_acc[acc]

            char.equip["Accessory 2"] = acc
            inventory.remove(acc)

            char.str += acc.str
            char.vit += acc.vit
            for n in arm.weak:
                    char.weak.append(n)
            char.dmg += wpn.dmg
        
        else:
            print ("No Accessories to equip.")


    pass

def removeEquip():
    
    char = chooseCharacter()
    if char == None:
            print("")
            return


    # ======================================
    print(f"What equipment are you removing from {char.name}\n")
    getEquip(char)
    slot = input("(W)eapon, (A)rmor, Accessory(1), or Accessory(2)?\n")

    if slot in cancelterms:
            print("")
            return None

    if slot.lower() == "w":
        
        if char.equip["Weapon"] == None:
            print(f"{char.name} has no weapon equipped.")

        else:
            wpn = char.equip["Weapon"]

            inventory.append(wpn)
            char.equip["Weapon"] = None

            char.str -= wpn.str
            char.dmg -= wpn.dmg

    elif slot.lower() == "a":
        
        if char.equip["Armor"] == None:
            print(f"{char.name} has no armor equipped.")

        else:
            arm = char.equip["Armor"]

            inventory.append(arm)
            char.equip["Armor"] = None

            char.str -= arm.str
            char.vit -= arm.vit
            # for n in arm.weak:
            #     char.weak.remove(n)

    elif slot.lower() == "1":
        
        if char.equip["Accessory 1"] == None:
            print(f"{char.name} has no Accessory equipped.")

        else:
            acc = char.equip["Accessory 1"]

            inventory.append(acc)
            char.equip["Accesory 1"] = None

            char.str -= acc.str
            char.vit -= acc.vit
            for n in arm.weak:
                char.weak.remove(n)

            char.dmg -= wpn.dmg

    elif slot.lower() == "2":
        
        if char.equip["Accessory 2"] == None:
            print(f"{char.name} has no Accessory equipped.")

        else:
            acc = char.equip["Accessory 2"]

            inventory.append(acc)
            char.equip["Accesory 2"] = None

            char.str -= acc.str
            char.vit -= acc.vit
            for n in arm.weak:
                char.weak.remove(n)

            char.dmg -= wpn.dmg


    pass

cancelterms = ["no","back","cancel","return","quit"]
# GAME

def runEquipment():
    testing_equip = True
    while testing_equip == True:

        os.system("cls")

        # SHOW PARTY LIST
        print ("Party:") #spacer
        for n in party:
            print (f"{n.name}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} /// TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        print ("") #spacer

        equip_command = input("What do you want to do? \n (E)quip \n (U)nequip \n Check (I)nventory\n Check (C)haracter's Status \n Check (S)kills \n (R)ecover HP \n or (Q)uit management\n").lower()



        if equip_command == "e":
            
            changeEquip()

            pass

        if equip_command == "i":
            getInventory()

        if equip_command == "u":
            
            removeEquip()

        if equip_command == "c":

            getStatus()

        if equip_command == "q":
            os.system("cls")
            testing_equip = False
        
        if equip_command == "s":
            getSkills()

        if equip_command == "r":
            partyRecovery()


        input("\nType anything to continue: ")


# GAME TEST
# runEquipment()