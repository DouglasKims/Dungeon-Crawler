import CombatSystem
import os



# LOGIC

class Equipment():
    def __init__(self,name,type,level,special,atk,dmg,dfn,weak,resist):
        self.name = name
        self.type = type
        self.level = level
        self.special = special
        self.atk = atk
        self.dmg = dmg
        self.dfn = dfn
        self.weak = weak
        self.resist = resist

# Equip types: Armor, Weapon, Accessory

loot1 = Equipment("Leather Armor","Armor",1,None,0,0,1,[CombatSystem.elem[1]],None)
loot2 = Equipment("Longsword +1","Weapon",2,"Dmg +",2,2,0,None,None)
loot2a = Equipment("Longsword +2","Weapon",3,"Dmg ++",3,3,0,None,None)
loot3 = Equipment("Shield","Accessory",1,None,-1,0,5,None,None)
loot4 = Equipment("Magic Ring","Accessory",1,"tec+",0,0,1,None,None)




inventory = [loot1,loot2,loot2a,loot3,loot4]

def chooseCharacter():
    print("Which Character are you managing?")
    for n in CombatSystem.party:
        print (f"({CombatSystem.party.index(n)}) {n.name}")
    char = input()
    
    if char in cancelterms:
            print("")
            return None
    
    try:
        char = int(char)
    except ValueError:
        char = None

    

    if char in range(0,len(CombatSystem.party)):
        char = CombatSystem.party[char]
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

    print(f"{char.name}'s Status\n Class: {char.char_class} // PLevel: {char.plevel}\n HP: {char.hp} / {char.maxhp}\n FP: {char.fp} / {char.maxfp}\n ATK: {char.atk} (DMG: {char.dmg})\n DEF: {char.dfn}\n TEC: {char.tec}\n SPD: {char.spd}\n LCK: {char.lck}\n")
    # getEquip func
    getEquip(char)

def getInventory():

    for n in inventory:
        print (f"({inventory.index(n)}) {n.name} // Type: {n.type} // Atk: {n.atk} (Dmg: {n.dmg}) // Dfn: {n.dfn} // Weak: {n.weak} // Resist: {n.resist} // Special: {n.special}")

    # for index, item in enumerate(inventory):
    #     print(f"({index}) {item.name} // Type: {item.type} // Atk: {item.atk} (Dmg: {item.dmg}) // Dfn: {item.dfn} // Weak: {item.weak} // Resist: {item.resist} // Special: {item.special}")

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
                    print (f"({list_weapon.index(n)}) {n.name} // Atk: {n.atk} // Special: {n.special}")

                try:
                    wpn = int(input())
                except ValueError:
                    wpn = None

                if wpn in range(0,len(list_weapon)):
                    wpn = list_weapon[wpn]

                char.equip["Weapon"] = wpn
                inventory.remove(wpn)

                char.atk += wpn.atk
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
                    print (f"({list_armor.index(n)}) {n.name} // Dfn: {n.dfn} // Special: {n.special} // Weak to: {n.weak} // Resists: {n.resist}")

                try:
                    arm = int(input())
                except ValueError:
                    arm = None

                if arm in range(0,len(list_armor)):
                    arm = list_armor[arm]

                char.equip["Armor"] = arm
                inventory.remove(arm)

                char.dfn += arm.dfn
                for n in arm.weak:
                    char.weak.append(n)
            
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
                    print (f"({list_acc.index(n)}) {n.name} // Atk: {n.atk} // Dfn: {n.dfn} // Special: {n.special} // Weak to: {n.weak} // Resists: {n.resist}")

                try:
                    acc = int(input())
                except ValueError:
                    acc = None

                if acc in range(0,len(list_acc)):
                    acc = list_acc[acc]

                char.equip["Accessory 1"] = acc
                inventory.remove(acc)

                char.atk += acc.atk
                char.dfn += acc.dfn
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
                print (f"({list_acc.index(n)}) {n.name} // Atk: {n.atk} // Dfn: {n.dfn} // Special: {n.special} // Weak to: {n.weak} // Resists: {n.resist}")

            try:
                acc = int(input())
            except ValueError:
                acc = None

            if acc in range(0,len(list_acc)):
                acc = list_acc[acc]

            char.equip["Accessory 2"] = acc
            inventory.remove(acc)

            char.atk += acc.atk
            char.dfn += acc.dfn
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

            char.atk -= wpn.atk
            char.dmg -= wpn.dmg

    elif slot.lower() == "a":
        
        if char.equip["Armor"] == None:
            print(f"{char.name} has no armor equipped.")

        else:
            arm = char.equip["Armor"]

            inventory.append(arm)
            char.equip["Armor"] = None

            char.atk -= arm.atk
            char.dfn -= arm.dfn
            for n in arm.weak:
                char.weak.remove(n)

    elif slot.lower() == "1":
        
        if char.equip["Accessory 1"] == None:
            print(f"{char.name} has no Accessory equipped.")

        else:
            acc = char.equip["Accessory 1"]

            inventory.append(acc)
            char.equip["Accesory 1"] = None

            char.atk -= acc.atk
            char.dfn -= acc.dfn
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

            char.atk -= acc.atk
            char.dfn -= acc.dfn
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

        equip_command = input("What do you want to do? \n (E)quip \n (U)nequip \n (C)heck Inventory\n Check Character (S)tatus \n (V)isit the Shop\n or (Q)uit management\n")



        if equip_command.lower() == "e":
            
            changeEquip()

            pass

        if equip_command.lower() == "c":
            getInventory()

        if equip_command.lower() == "u":
            
            removeEquip()

        if equip_command.lower() == "s":

            getStatus()

        if equip_command.lower() == "q":
            return

        # for n in CombatSystem.party:
        #     print(f"{n.name} is part of the party.")

        input("\nType anything to continue: ")


# GAME TEST
# runEquipment()
    




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