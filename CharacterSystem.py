
import os
import math
import copy
import random

# CHaracters


class Character:
    def __init__(self,name,char_class,race,level,maxhp,hp,maxtp,tp,str,dmg,tec,vit,agi,lck,slist,acted,defending,weak,equip,exp,init):
        self.name = name
        self.char_class = char_class
        self.race = race
        self.level = level
        self.maxhp = maxhp
        self.hp = hp
        self.maxtp = maxtp
        self.tp = tp
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
    def __init__(self,name,hp,tp,str,dmg,tec,vit,agi,lck,special,improv,lore):
        self.name = name
        self.hp = hp
        self.tp = tp
        self.str = str
        self.dmg = dmg
        self.tec = tec
        self.vit = vit
        self.agi = agi
        self.lck = lck
        self.special = special
        self.improv = improv
        self.lore = lore

class CharacterRace:
    def __init__(self, name, bonus, hiddenbonus, lore):
        self.name = name
        self.bonus = bonus
        self.hiddenbonus = hiddenbonus
        self.lore = lore

# CHARACTER CLASSES
knight = CharacterClass(
    name = "Knight",
    hp = 10,
    tp = 2,
    str = 6,
    dmg = 2,
    tec = 2,
    vit = 5,
    agi = 3,
    lck = 3,
    improv = [4/3, 1/2, 1, 1/3, 1, 3/5, 1/3],
    special = None,
    lore = "A capable fighter with high attack and defense, know a few combat tactics, but doesn't excels in special techniques.")
thaumaturge = CharacterClass(
    "Thaumaturge",
    hp = 6,
    tp = 5,
    str = 4,
    dmg = 1,
    tec = 6,
    vit = 2,
    agi = 2,
    lck = 4,
    improv = [2/3, 1, 2/3, 1, 2/3, 2/5, 2/3],
    special = None,
    lore = "A capable combatant who's reliable in physical combat, but really excells at support and healing.")
arcanist = CharacterClass(
    "Arcanist",
    hp = 4,
    tp = 7,
    str = 2,
    dmg = 1,
    tec = 8,
    vit = 1,
    agi = 4,
    lck = 2,
    improv = [1/3, 3/2, 1/4, 3/2, 1/3, 2/3, 1/2],
    special = None,
    lore = "A specialist combatant, really weak and fragile, but can use devastating special techniques and elemental attacks.")
scout = CharacterClass(
    "Scout",
    hp = 6,
    tp = 3,
    str = 3,
    dmg = 2,
    tec = 4,
    vit = 2,
    agi = 8,
    lck = 8,
    improv = [1/2, 1/3, 1/2, 1/2, 1/2, 3/2, 4/3],
    special = None,
    lore = "A stealthy combatant, somewhat weak and fragile, but capable of landing powerful critical attacks more frequently than others.")
herald = CharacterClass(
    "Herald",
    hp = 8,
    tp = 4,
    str = 5,
    dmg = 1,
    tec = 5,
    vit = 3,
    agi = 5,
    lck = 5,
    improv = [3/4, 2/3, 1, 3/4, 2/3, 2/3, 2/3],
    special = None,
    lore = "A well-rounded combatant and explorer, able to use offensive and support abilities, but doesn't really excels in any.")
quartermaster = CharacterClass(
    "Quartermaster",
    hp = 6,
    tp = 3,
    str = 4,
    dmg = 1,
    tec = 2,
    vit = 4,
    agi = 5,
    lck = 5,
    improv = [1, 1/4, 1, 1/3, 1, 1/2, 1],
    special = None,
    lore = "A supportive combatant, not very powerful in combat, but able to make exploration easier with many support skills.")

character_classes = [knight,thaumaturge,arcanist,scout,herald,quartermaster]

# CHARACTER RACES
r_human = CharacterRace(
    name = "Human", bonus = "+1 to Random stat", hiddenbonus = "+1 to Random stat every even level",
    lore = "The most varied species in the kingdoms. They can do almost literaly everything, but it's hard to pinpoint any one human's talents.")
r_dwarf = CharacterRace(
    name = "Dwarf", bonus = "+5 Max HP", hiddenbonus = "+3 Max HP / Level",
    lore = "Short and Stout, Dwarves are very resilient and won't go down easily, which is why despite their short stature, they're usually found in the frontlines.")
r_orc = CharacterRace(
    name = "Orc", bonus = "+1 Dmg", hiddenbonus = "+1 DMG every 5 levels.",
    lore = "Orcs can channel a mighty strenght from their naturaly strong bodies, which allows them to hit harder and cause more physical damge.")
r_faefolk = CharacterRace(
    name = "Faefolk", bonus = "+5 TP", hiddenbonus = "+1 Max TP / Level",
    lore = "Elves, Centaurs, Satyrs, Duendes, and other such creatures constitues the Faefolk, they have a natural penchant for magic, which comes easily for them.")
r_dragonkin = CharacterRace(
    name = "Dragonkin", bonus = "+1 STR", hiddenbonus = "+1 STR or TEC every even level",
    lore = "Tall and imposing, Dragonkin are naturaly strong and resilient to magic, which is why they really shine in the frontlines of combat.")
r_beastfolk = CharacterRace(
    name = "Beastfolk", bonus = "+1 VIT", hiddenbonus = "+1 AGI or LCK every even level",
    lore = "Animal folk are many and varied, but their animalistic features makes them more resilient and faster than most other races.") 
r_tiefling = CharacterRace(
    name = "Tiefling", bonus = "+1 TEC", hiddenbonus = "+1 TEC or +1 Max TP every even even level",
    lore = "These humanoids with an infernal heritage have demonic features, but also higher magical resistence and a natural inclination for magical studies.")

character_races = [r_human,r_dwarf,r_orc,r_faefolk,r_dragonkin,r_beastfolk,r_tiefling]

drav = Character(
    name = "Dravroth", char_class = herald, race = r_dragonkin,
    level = 1, maxhp = 80, hp = 80, maxtp = 40, tp = 40,
    str = 6, dmg = 1, tec = 6, vit = 2, agi = 5, lck = 6,
    slist =  ["leas","pas","comas","grun"],
    acted = False, defending = False, weak = [], exp = 0, init = 0,
    equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None})
dan = Character(
    name = "Thorudan", char_class= thaumaturge, race = r_faefolk,
    level=1, maxhp=60, hp=60, maxtp=50, tp=50,
    str = 4, dmg = 1, tec = 10, vit = 2, agi = 3, lck = 3,
    slist = ["leas","cruai","igg","gaa","grun","comas"],
    acted = False, defending = False, weak = [], exp = 0, init = 0,
    equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None})
mars = Character(
    name = "Mars", char_class = knight, race = r_orc,
    level = 1, maxhp = 100, hp = 100, maxtp = 20, tp = 20,
    str = 8, dmg = 2, tec = 3, vit = 4, agi = 3, lck = 3,
    slist = ["leas","yab","grun"],
    acted= False, defending = False, weak = [], exp = 0, init = 0,
    equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None})
eck = Character(
    name="Eckbert", char_class= scout, race = r_faefolk,
    level=1, maxhp=60, hp=60, maxtp=30, tp=30,
    str=3, dmg=2, tec=4, vit=2, agi=8, lck=8,
    slist=[], acted=False, defending=False, weak=[], exp=0, init=0,
    equip={
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None})

charTemplate = Character(
    name="Name", char_class="Class", race = None,
    level=1, maxhp=10, hp=10, maxtp=10, tp=10,
    str=1, dmg=1, tec=1, vit=1, agi=1, lck=1,
    slist=[], acted=False, defending=False, weak=[], exp=0, init=0,
    equip={
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None})


character_roster = [drav, dan, mars, eck]

elem = ["phys","fire","wind","earth","ice","thunder","toxic","decay","chaos","death"]

party = [drav,dan,mars,eck]
party_money = 0

cancelterms = ["no","back","cancel","return","quit"]

def checkLevel(char):

    while char.exp >= char.level*1000*1.5:
        os.system("cls")
        print(f"{char.name} has leveled up to level {char.level+1}!")
        levelUpChar(char)

def pickClass(cname):
    for n in character_classes:
        if n == cname:
            return n

def levelUpChar(char):
    class_choice = pickClass(char.char_class)
    choice_made = False
    char.level += 1
    
    #Increase base stats
    print(f"{char.name}'s stats have improved!\n Max HP: {math.floor(char.maxhp)} >>> {math.floor(char.maxhp+(class_choice.improv[0]*class_choice.hp))} // Max TP: {math.floor(char.maxtp)} >>> {math.floor(char.maxtp+(class_choice.improv[1]*class_choice.tp))}\n STR: {math.floor(char.str)} >>> {math.floor(char.str+class_choice.improv[2])} // TEC: {math.floor(char.tec)} >>> {math.floor(char.tec+class_choice.improv[3])} // VIT: {math.floor(char.vit)} >>> {math.floor(char.vit+class_choice.improv[4])} // AGI: {math.floor(char.agi)} >>> {math.floor(char.agi+class_choice.improv[5])} // LCK: {math.floor(char.lck)} >>> {math.floor(char.lck+class_choice.improv[6])}\n")
    char.maxhp += class_choice.improv[0]*class_choice.hp
    char.hp += class_choice.improv[0]*class_choice.hp
    char.maxtp += class_choice.improv[1]*class_choice.tp
    char.tp += class_choice.improv[1]*class_choice.tp
    char.str += class_choice.improv[2]
    char.tec += class_choice.improv[3]
    char.vit += class_choice.improv[4]
    char.agi += class_choice.improv[5]
    char.lck += class_choice.improv[6]


    while choice_made == False:
    
        choice = input(f"Choose one stat to improve:\n Max (H)P: {math.floor(char.maxhp)} >>> {math.floor(char.maxhp+class_choice.hp)}\n Max (TP): {math.floor(char.maxtp)} >>> {math.floor(char.maxtp+class_choice.tp)}\n (S)tr: {math.floor(char.str)} >>> {math.floor(char.str+1)}\n (T)ec: {math.floor(char.tec)} >>> {math.floor(char.tec+1)}\n (V)it: {math.floor(char.vit)} >>> {math.floor(char.vit+1)}\n (A)gi: {math.floor(char.agi)} >>> {math.floor(char.agi+1)}\n (L)ck: {math.floor(char.lck)} >>> {math.floor(char.lck+1)}\n\n")

        if choice.lower() == "h":
            final_choice = input(f"\nThis will increase your Max HP by {math.floor(class_choice.hp)}.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y" or final_choice.lower == "yes":
                char.maxhp += class_choice.hp
                char.hp += class_choice.hp
                choice_made = True

            if final_choice.lower() == "n":
                pass
    
        elif choice.lower() == "tp":
            final_choice = input(f"\nThis will increase your Max TP by {math.floor(class_choice.tp)}.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y" or final_choice.lower == "yes":
                char.maxtp += class_choice.tp
                char.tp += class_choice.tp
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "s":
            final_choice = input(f"\nThis will increase your Str by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y" or final_choice.lower == "yes":
                char.str += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "t":
            final_choice = input(f"\nThis will increase your Tec by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y" or final_choice.lower == "yes":
                char.tec += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "v":
            final_choice = input(f"\nThis will increase your Vit by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y" or final_choice.lower == "yes":
                char.vit += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "a":
            final_choice = input(f"\nThis will increase your agi by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y" or final_choice.lower == "yes":
                char.agi += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass

        elif choice.lower() == "l":
            final_choice = input(f"\nThis will increase your Lck by 1.\n Proceed? (Y/N)\n")
            if final_choice.lower() == "y" or final_choice.lower == "yes":
                char.lck += 1
                choice_made = True

            if final_choice.lower() == "n":
                pass

def createCharacter():

    newchar = None

    os.system("cls")

    for n in character_races:
        print(f"({character_races.index(n)}) {n.name} / Bonus: {n.bonus}")
        print(f"  {n.lore}")

    choice_race = input ("What race will the new character have? (type 'no' to cancel)  \n")

    if choice_race in cancelterms:
        return None
    elif int(choice_race) in range(0,len(character_races)):
        choice_race = int(choice_race)

    os.system("cls")

    for n in character_classes:
        print(f"({character_classes.index(n)}) {n.name} / HP: {n.hp*10} / TP : {n.tp*10}")
        print(f"  STR: {n.str} (Dmg: {n.dmg}) / TEC: {n.tec} / VIT: {n.vit} / AGI: {n.agi} / LCK: {n.lck}")
        print(f"  {n.lore}")

    

    choice_class = input ("What class will the new character have? (type 'no' to cancel)  \n")

    if choice_class in cancelterms:
        return None
    elif int(choice_class) in range(0,len(character_classes)):
        choice_class = int(choice_class)

    os.system("cls")

    choice_name = "New Character's name here"
    print("\n")
    while len(choice_name) > 12:
        choice_name = input ("What will be the new character's name? (type 'no' to cancel)  ")

        if choice_name in cancelterms:
            return None
        elif len(choice_name) > 12:
            print("Name is too long, try something shorter (up to 12 characters)\n")

    newchar = Character(
        name = choice_name, char_class = character_classes[choice_class], race = character_races[choice_race],
        maxhp = character_classes[choice_class].hp * 10, hp = character_classes[choice_class].hp * 10 , maxtp = character_classes[choice_class].tp * 10, tp = character_classes[choice_class].tp * 10,
        str = character_classes[choice_class].str, dmg = character_classes[choice_class].dmg, tec = character_classes[choice_class].tec, vit = character_classes[choice_class].vit, agi = character_classes[choice_class].agi, lck = character_classes[choice_class].lck,
        slist = [], acted = False, defending = False, weak = [], level = 1, exp = 0, init = 0,
        equip = {
            "Weapon":None,
            "Armor":None,
            "Accessory 1":None,
            "Accessory 2":None})
    
    if newchar is not None:
        if newchar.race == r_human:
            randomstat = random.choice["str","tec","vit","agi","lck"]
            if randomstat == "str":
                newchar.str += 1
            elif randomstat == "tec":
                newchar.tec += 1
            elif randomstat == "vit":
                newchar.vit += 1
            elif randomstat == "agi":
                newchar.agi += 1
            elif randomstat == "lck":
                newchar.lck += 1

        elif newchar.race == r_dwarf:
            newchar.maxhp += 5
            newchar.hp += 5

        elif newchar.race == r_orc:
            newchar.dmg += 1
        
        elif newchar.race == r_faefolk:
            newchar.maxtp += 5
            newchar.tp += 5

        elif newchar.race == r_dragonkin:
            newchar.str += 1

        elif newchar.race == r_beastfolk:
            newchar.vit += 1
        
        elif newchar.race == r_tiefling:
            newchar.tec += 1
            
    
    print (f"\n{newchar.name}, {newchar.race.name} {newchar.char_class.name}")
    print (f"  HP : {newchar.hp} / TP : {newchar.tp}\n  STR: {newchar.str} (DMG: {newchar.dmg}) / TEC: {newchar.tec} / VIT: {newchar.vit} / AGI: {newchar.agi} / LCK: {newchar.lck}")

    choice_final = input ("\nIs this the character you want? (type 'no' to cancel)")

    if choice_final in cancelterms:
        return None
    else:
        character_roster.append(copy.deepcopy(newchar))
        input(f"Character {newchar.name} has been added to the roster. Type anything to continue.  ")
        return
    pass

def runRoster():
    testing_characters = True

    while testing_characters:
        
        print (f"\nThere are {len(character_roster)} characters in the roster.")

        command = input(f"What do you want to do?\n Create a (N)ew Character, check the (R)oster, or (Q)uit?").lower()

        if command in ["r", "roster"]:

            for index, char in enumerate(character_roster):
                print (f"({character_roster.index(char)}) {char.name}: a {char.race.name} {char.char_class.name}.")

            choice_roster = input("Inspect any character further?")

            if int(choice_roster) in range (len(character_roster)):

                char = character_roster[int(choice_roster)]

                print(f"\n{char.name}'s Status\n Race: {char.race.name} / Class: {char.char_class.name} / Level: {char.level} ({round(char.exp)} / {round(char.level*200*1.5)} EXP)\n HP: {math.floor(char.hp)} / {math.floor(char.maxhp)} // TP: {math.floor(char.tp)} / {math.floor(char.maxtp)}\n STR: {math.floor(char.str)} (DMG: {char.dmg}) / TEC: {math.floor(char.tec)} / VIT: {math.floor(char.vit)} / AGI: {math.floor(char.agi)} / LCK: {math.floor(char.lck)}\n")

            else:
                pass
            
        elif command in ["n","new"]:

            createCharacter()

        elif command in ["q", "quit"]:
            testing_characters = False


# TESTING
# runRoster()


####