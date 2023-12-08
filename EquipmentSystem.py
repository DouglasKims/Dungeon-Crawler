import math
import os
import copy


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


# LOGIC

class Equipment():
    def __init__(self,name,type,level,special,str,dmg,vit,tec,agi,lck,weak,resist,value,lore):
        self.name = name
        self.type = type
        self.level = level
        self.special = special
        self.str = str
        self.dmg = dmg
        self.tec = tec
        self.vit = vit
        self.agi = agi
        self.lck = lck
        self.weak = weak
        self.resist = resist
        self.value = value
        self.lore = lore

class Consumable():
    def __init__(self, name, type, lore, value):
        self.name = name
        self.type = type
        self.lore = lore
        self.value = value

# Equip types: Armor, Weapon, Accessory

armor1 = Equipment("Cloth Armor","Armor",1,None,str=0,dmg=0,tec=0,vit=1,agi=1,lck=0,weak=None,resist=None,value=20,
                   lore="Simple armor that provides minimal protection to wearer, but allows good freedom of movement.")
armor2 = Equipment("Chain Mail","Armor",1,None,str=0,dmg=0,tec=0,vit=2,agi=0,lck=0,weak=None,resist=None,value=50,
                   lore="Simple armor that offers decent protection, but too heavy for the untrained to wear.")
weapon1 = Equipment("Simple Blade","Weapon",1,None,str=1,dmg=0,tec=0,vit=0,agi=0,lck=0,weak=None,resist=None,value=10,
                    lore="Simple weapon that offers basic means of offense and wieldy enough for anyone to use.")
weapon2 = Equipment("Sturdy Branch","Weapon",1,None,str=0,dmg=0,tec=1,vit=0,agi=0,lck=0,weak=None,resist=None,value=20,
                    lore="An ordinary tree branch inscribed with runes to facilitate the use of techniques in combat.")
weapon3 = Equipment("Sharpened Blade","Weapon",1,None,str=3,dmg=1,tec=0,vit=0,agi=0,lck=0,weak=None,resist=None,value=80,
                    lore="A weapon made to inflict grievous wounds and shorten the duration of battles.")
acc1 = Equipment("Round Shield","Accessory",1,None,str=-2,dmg=0,tec=0,vit=2,agi=-1,lck=0,weak=None,resist=None,value=30,
                    lore="A large pot lid repurposed into a shield. Not the sturdiest, but can still deflect some blows.")
acc2 = Equipment("Focus Ring","Accessory",1,None,str=0,dmg=0,tec=1,vit=0,agi=0,lck=0,weak=None,resist=None,value=50,
                    lore="A ring inscribed with runes that assists the wielder in remembering techniques in combat.")
acc3 = Equipment("Lucky Charm","Accessory",1,None,str=0,dmg=0,tec=0,vit=0,agi=0,lck=1,weak=None,resist=None,value=50,
                    lore="An amulet decorated with symbols of luck, said to work even for non-believers.")
acc4 = Equipment("Fire Ring","Accessory",1,None,str=0,dmg=0,tec=0,vit=0,agi=0,lck=0,weak=None,resist=["fire"],value=50,
                    lore="A charred and blackened ring that increases the user's protection to fire.")

item1 = Consumable("Healing Draught","Healing","Heal 30 HP",10)
item2 = Consumable("Invigorating Tonic","Healing","Heal 15 tp",50)
item3 = Consumable("Charged Memento","Reviving","Revives with 25% HP", 50)
item4 = Consumable("Rations","Rest","Eating these in a safe place will recover half HP and TP to the party.", 50)
item5 = Consumable("Urn of Ret","Return","Breaking this urn releases the magical powder that returns the party to town.", 50)

# SHOP STOCK
shop_stock = [armor1, armor2,weapon1,weapon2,acc1,acc2,acc3,acc4,item1,item2,item3,item4,item5]

# EQUIPMENT
inventory = []

# CONSUMABLES
consumables = []



def chooseCharacter():
    from CharacterSystem import party as party
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
    
    from CombatSystem import fetchSkills
    fetchSkills(char)

def partyRecovery():
    from CharacterSystem import party as party
    tpcost = 0
    totaltp = 0
    totaltpcost = 0

    for n in party:
        if n.hp <= 0:
            tpcost += 15
            totaltp += n.tp
        elif n.hp < n.maxhp:
            tpcost += (n.hp - n.maxhp)* -1/20 + 1
            totaltp += n.tp
        else:
            totaltp += n.tp

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
        print (f"    ({consumables.index(n)}) {n.name} // Type: {n.type} // Effect: {n.lore} // Value: {n.value} Cr")

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
    from CharacterSystem import party as party

    if item.type == "Healing":
        iname, ipower, ieffect = item.lore.split()
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
            return True

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
            return True

    if item.type == "Reviving":
        ieffect, i1, ipower, i2 = item.lore.split()

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
        return True

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
                char.tec += wpn.tec
                char.vit += wpn.vit
                char.agi += wpn.agi
                char.lck += wpn.lck
                if wpn.weak is not None:
                    for n in wpn.weak:
                        char.weak.append(n)
                if wpn.resist is not None:
                    for n in wpn.resist:
                        char.resist.append(n)
            
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

                char.str += arm.str
                char.dmg += arm.dmg
                char.tec += arm.tec
                char.vit += arm.vit
                char.agi += arm.agi
                char.lck += arm.lck
                if arm.weak is not None:
                    for n in arm.weak:
                        char.weak.append(n)
                if arm.resist is not None:
                    for n in arm.resist:
                        char.resist.append(n)
            
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
                char.dmg += acc.dmg
                char.tec += acc.tec
                char.vit += acc.vit
                char.agi += acc.agi
                char.lck += acc.lck
                if acc.weak is not None:
                    for n in acc.weak:
                        char.weak.append(n)
                if acc.resist is not None:
                    for n in acc.resist:
                        char.resist.append(n)

            
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
            char.dmg += acc.dmg
            char.tec += acc.tec
            char.vit += acc.vit
            char.agi += acc.agi
            char.lck += acc.lck
            if acc.weak is not None:
                for n in acc.weak:
                    char.weak.append(n)
            if acc.resist is not None:
                for n in acc.resist:
                    char.resist.append(n)
    
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
            char.tec -= wpn.tec
            char.vit -= wpn.vit
            char.agi -= wpn.agi
            char.lck -= wpn.lck
            if wpn.weak is not None:
                for n in wpn.weak:
                    if n in char.weak:
                        char.weak.remove(n)
            if wpn.resist is not None:
                for n in wpn.resist:
                    if n in char.resist:
                        char.resist.remove(n)

    elif slot.lower() == "a":
        
        if char.equip["Armor"] == None:
            print(f"{char.name} has no armor equipped.")

        else:
            arm = char.equip["Armor"]

            inventory.append(arm)
            char.equip["Armor"] = None

            char.str -= arm.str
            char.dmg -= arm.dmg
            char.tec -= arm.tec
            char.vit -= arm.vit
            char.agi -= arm.agi
            char.lck -= arm.lck
            if arm.weak is not None:
                for n in arm.weak:
                    if n in char.weak:
                        char.weak.remove(n)
            if arm.resist is not None:
                for n in arm.resist:
                    if n in char.resist:
                        char.resist.remove(n)

    elif slot.lower() == "1":
        
        if char.equip["Accessory 1"] == None:
            print(f"{char.name} has no Accessory equipped.")

        else:
            acc = char.equip["Accessory 1"]

            inventory.append(acc)
            char.equip["Accesory 1"] = None

            char.str -= acc.str
            char.dmg -= acc.dmg
            char.tec -= acc.tec
            char.vit -= acc.vit
            char.agi -= acc.agi
            char.lck -= acc.lck
            if acc.weak is not None:
                for n in acc.weak:
                    if n in char.weak:
                        char.weak.remove(n)
            if acc.resist is not None:
                for n in acc.resist:
                    if n in char.resist:
                        char.resist.remove(n)

    elif slot.lower() == "2":
        
        if char.equip["Accessory 2"] == None:
            print(f"{char.name} has no Accessory equipped.")

        else:
            acc = char.equip["Accessory 2"]

            inventory.append(acc)
            char.equip["Accesory 2"] = None

            char.str -= acc.str
            char.dmg -= acc.dmg
            char.tec -= acc.tec
            char.vit -= acc.vit
            char.agi -= acc.agi
            char.lck -= acc.lck
            if acc.weak is not None:
                for n in acc.weak:
                    if n in char.weak:
                        char.weak.remove(n)
            if acc.resist is not None:
                for n in acc.resist:
                    if n in char.resist:
                        char.resist.remove(n)


    pass

cancelterms = ["no","back","cancel","return","quit"]
# GAME

def runEquipment():
    import CharacterSystem
    from CharacterSystem import party as party
    testing_equip = True
    while testing_equip == True:

        os.system("cls")

        # SHOW PARTY LIST
        print ("Party:") #spacer
        for n in party:
            if n.hp <= 0:
                print (f"{BG_RED}{n.name}{RESET}'s HP: DEAD/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")    
            else:
                print (f"{n.name}'s HP: {math.floor(n.hp)}/{math.floor(n.maxhp)} // TP: {math.floor(n.tp)}/{math.floor(n.maxtp)}")
        print ("") #spacer
        print (f"Party Funds: {CharacterSystem.party_money} Crowns\n")

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