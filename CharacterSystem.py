
import os
import math
import copy
import random
import EquipmentSystem

## SKILLS
global_skill_list = {
    "firo": (1, "Causes weak fire damage to one enemy.", 4),
    "grunfiro": (1, "Causes weak fire damage to all enemies.", 10),
    "firomor": (1, "Causes moderate fire damage to one enemy.", 8),
    "grunfiromor": (1, "Causes moderate fire damage to all enemies.", 16),
    "firomatha": (1, "Causes heavy fire damage to one enemy.", 12),
    "grunfiromatha": (1, "Causes heavy fire damage to all enemies.", 22),
    
    "gelo": (1, "Causes weak ice damage to one enemy.", 4),
    "grungelo": (1, "Causes weak ice damage to all enemies.", 10),
    "gelomor": (1, "Causes moderate ice damage to one enemy.", 8),
    "grungelomor": (1, "Causes moderate ice damage to all enemies.", 16),
    "gelomatha": (1, "Causes heavy ice damage to one enemy.", 12),
    "grungelomatha": (1, "Causes heavy ice damage to all enemies.", 22),

    "gale": (1, "Causes weak wind damage to one enemy.", 4),
    "grungale": (1, "Causes weak wind damage to all enemies.", 10),
    "galemor": (1, "Causes moderate wind damage to one enemy.", 8),
    "grungalemor": (1, "Causes moderate wind damage to all enemies.", 16),
    "galematha": (1, "Causes heavy wind damage to one enemy.", 12),
    "grungalematha": (1, "Causes heavy wind damage to all enemies.", 22),

    "tera": (1, "Causes weak earth damage to one enemy.", 4),
    "gruntera": (1, "Causes weak earth damage to all enemies.", 10),
    "teramor": (1, "Causes moderate earth damage to one enemy.", 8),
    "grunteramor": (1, "Causes moderate earth damage to all enemies.", 16),
    "teramatha": (1, "Causes heavy earth damage to one enemy.", 12),
    "grunteramatha": (1, "Causes heavy earth damage to all enemies.", 22),


    "volt": (1, "Causes weak thunder damage to one enemy.", 4),
    "grunvolt": (1, "Causes weak thunder damage to all enemies.", 10),
    "voltmor": (1, "Causes moderate thunder damage to one enemy.", 8),
    "grunvoltmor": (1, "Causes moderate thunder damage to all enemies.", 16),
    "voltmatha": (1, "Causes heavy thunder damage to one enemy.", 12),
    "grunvoltmatha": (1, "Causes heavy thunder damage to all enemies.", 22),

    "veno": (1, "Causes weak toxic damage to one enemy.", 4),
    "grunveno": (1, "Causes weak toxic damage to all enemies.", 10),
    "venomor": (1, "Causes moderate toxic damage to one enemy.", 8),
    "grunvenomor": (1, "Causes moderate toxic damage to all enemies.", 16),
    "venomatha": (1, "Causes heavy toxic damage to one enemy.", 12),
    "grunvenomatha": (1, "Causes heavy toxic damage to all enemies.", 22),
    
    "cura": (1, "Restores small amount of health to one ally.", 3, "S"),
    "gruncura": (1, "Restores small amount of health to all allies.", 7, "S"),
    "curamor": (1, "Restores moderate amount of health to one ally.", 7, "S"),
    "gruncuramor": (1, "Restores moderate amount of health to all allies.", 12, "S"),
    "curamatha": (1, "Restores full health to one ally.", 18, "S"),
    "gruncuramatha": (1, "Restores full health to all allies.", 30, "S"),
    
    "revita": (1, f"Revives one fallen ally with 30% of HP.", 7, "S"),
    "revitamor": (1, f"Revives one fallen ally with 60% of HP.", 10, "S"),
    "revitamatha": (1, f"Revives one fallen ally with full HP.", 18, "S"),
    
    "enhast": (1, "Enhances STR for one ally.", 3, "S"),
    "enhate": (1, "Enhances TEC for one ally.", 3, "S"),
    "enhavi": (1, "Enhances VIT for one ally.", 3, "S"),
    "enhagi": (1, "Enhances AGI for one ally.", 3, "S"),
    "enhalk": (1, "Enhances LCK for one ally.", 3, "S"),

    "enfest": (1, "Enhances STR for one ally.", 3, "S"),
    "enfete": (1, "Enhances TEC for one ally.", 3, "S"),
    "enfevi": (1, "Enhances VIT for one ally.", 3, "S"),
    "enfegi": (1, "Enhances AGI for one ally.", 3, "S"),
    "enfelk": (1, "Enhances LCK for one ally.", 3, "S"),

    "appraise": (1, "Increases EXP gain for slain enemies.", 20,"S"),
    "bomb": (1, "Causes nuke damage to all enemies.", 10),
    "coating": (1, "Grants elemental resistance to allies.", 10, "S"),

    "protect": (1, "Protects party from incoming damage.", 5, "S"),
    "decoy": (1, "Creates a decoy to divert attacks from party.", 15, "S"),

    ### PHYS SKILLS

    "charge": (1, "Attacks one enemy up to three times.", 0, 15),
    "cleave": (1, "Attacks random enemies up to five times.", 3, 20),
    
    "sneak": (1, "Attacks one enemy with increased damage and crit rate.", 3, 0),
    "hunt": (1, "Attacks one enemy with increased blah.", 3, 0),


}


# Characters
weapon1 = EquipmentSystem.weapon1
armor1 = EquipmentSystem.armor1

class Character:
    def __init__(self,name,char_class,race,level,maxhp,hp,maxtp,tp,str,dmg,tec,vit,agi,lck,slist,acted,defending,weak,resist,equip,exp,init,skillpts,perkpts, effects):
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
        self.resist = resist
        self.equip = equip
        self.exp = exp
        self.skillpts = skillpts
        self.perkpts = perkpts
        self.init = init
        self.effects = effects

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
    agi = 2,
    lck = 3,
    improv = [4/3, 1/2, 1, 1/3, 1, 3/5, 1/3, 1/6],
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
    improv = [2/3, 1, 2/3, 1, 2/3, 2/5, 2/3, 1/10],
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
    improv = [1/3, 3/2, 1/4, 3/2, 1/3, 2/3, 1/2, 1/15],
    special = None,
    lore = "A specialist combatant, really weak and fragile, but can use devastating special techniques and elemental attacks.")
scout = CharacterClass(
    "Scout",
    hp = 6,
    tp = 2,
    str = 5,
    dmg = 2,
    tec = 2,
    vit = 2,
    agi = 6,
    lck = 6,
    improv = [1/2, 1/3, 1/2, 1/2, 1/2, 3/2, 4/3, 1/8],
    special = None,
    lore = "A stealthy combatant, somewhat weak and fragile, but capable of landing powerful critical attacks more frequently than others.")
herald = CharacterClass(
    "Herald",
    hp = 6,
    tp = 3,
    str = 4,
    dmg = 1,
    tec = 4,
    vit = 3,
    agi = 4,
    lck = 4,
    improv = [3/4, 2/3, 1, 3/4, 2/3, 2/3, 2/3, 1/8],
    special = None,
    lore = "A well-rounded combatant and explorer, able to use offensive and support abilities, but doesn't really excels in any.")
quartermaster = CharacterClass(
    "Quartermaster",
    hp = 6,
    tp = 3,
    str = 4,
    dmg = 1,
    tec = 1,
    vit = 4,
    agi = 5,
    lck = 5,
    improv = [1, 1/4, 1, 1/3, 1, 1/2, 1, 1/6],
    special = None,
    lore = "A supportive combatant, not very powerful in combat, but able to make exploration easier with many support skills.")

character_classes = [knight,thaumaturge,arcanist,scout,herald,quartermaster]

# CHARACTER RACES
r_human = CharacterRace(
    name = "Human", bonus = "+1 to LCK", hiddenbonus = "+1 to Random stat every even level",
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
    acted = False, defending = False, weak = [], resist = [], exp = 0, init = 0, skillpts= 0, perkpts= 0, effects={},
    equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None},
    slist =  {
        "firo": global_skill_list["firo"],
        "cura": global_skill_list["cura"],
        "enhast": global_skill_list["enhast"] })
dan = Character(
    name = "Thorudan", char_class= thaumaturge, race = r_faefolk,
    level=1, maxhp=60, hp=60, maxtp=50, tp=50,
    str = 4, dmg = 1, tec = 10, vit = 2, agi = 3, lck = 3,
    acted = False, defending = False, weak = [], resist = [], exp = 0, init = 0, skillpts= 0, perkpts= 0, effects={},
    equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None},
    slist = {"tera": global_skill_list["tera"],
             "cura": global_skill_list["cura"],
             "revita": global_skill_list["revita"]})
mars = Character(
    name = "Mars", char_class = knight, race = r_orc,
    level = 1, maxhp = 100, hp = 100, maxtp = 20, tp = 20,
    str = 8, dmg = 2, tec = 3, vit = 4, agi = 3, lck = 3,
    acted= False, defending = False, weak = [], resist = [], exp = 0, init = 0, skillpts= 0, perkpts= 0,effects={},
    equip = {
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None},
    slist = {"charge": global_skill_list["charge"],
             "cleave": global_skill_list["cleave"],
             "protect": global_skill_list["protect"]},)
eck = Character(
    name="Eckbert", char_class= scout, race = r_faefolk,
    level=1, maxhp=60, hp=60, maxtp=30, tp=30,
    str=5, dmg=2, tec=4, vit=2, agi=8, lck=8,
    acted=False, defending=False, weak=[], resist = [], exp=0, init=0, skillpts= 0, perkpts= 0,effects={},
    equip={
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None},
    slist={"sneak": global_skill_list["sneak"],
           "decoy": global_skill_list["decoy"],
           "hunt": global_skill_list["hunt"]})

charTemplate = Character(
    name="Name", char_class="Class", race = None,
    level=1, maxhp=10, hp=10, maxtp=10, tp=10,
    str=1, dmg=1, tec=1, vit=1, agi=1, lck=1,
    acted=False, defending=False, weak=[], resist=[], exp=0, init=0, skillpts=0, perkpts=0,effects={},
    equip={
    "Weapon":None,
    "Armor":None,
    "Accessory 1":None,
    "Accessory 2":None},
    slist={})


character_roster = []

elem = ["phys","fire","wind","earth","ice","thunder","toxic","decay","chaos","death"]

party = [drav,dan,mars,eck]
party_money = 100

cancelterms = ["no","back","cancel","return","quit"]



def checkLevel(char):

    while char.exp >= char.level*1000: # *1.5
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
    char.dmg += class_choice.improv[7]


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
        acted = False, defending = False, weak = [], resist= [], level = 1, exp = 0, init = 0, skillpts=0, perkpts=0,
        equip = {
            "Weapon":weapon1,
            "Armor":armor1,
            "Accessory 1":None,
            "Accessory 2":None},
        slist = {}, effects = {})
    
    if newchar is not None: # Extra Stats per Race
        if newchar.race == r_human:
            # randomstat = random.choice(["str","tec","vit","agi","lck"])
            # if randomstat == "str":
            #     newchar.str += 1
            # elif randomstat == "tec":
            #     newchar.tec += 1
            # elif randomstat == "vit":
            #     newchar.vit += 1
            # elif randomstat == "agi":
            #     newchar.agi += 1
            # elif randomstat == "lck":
            #     newchar.lck += 1
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
            
    if newchar is not None: # Extra Skills per Class

        if newchar.char_class == arcanist:
            choosingskill = True
            while choosingskill:
                os.system("cls")
                print (f"\nElements: Fire, Ice, Wind, Earth, Thunder, Toxic")
                choice = input(f"What element is {newchar.name} attuned to?  ").lower()

                if choice == "fire":
                    newchar.slist["firo"] = global_skill_list["firo"]
                    choosingskill = False

                if choice == "ice":
                    newchar.slist["gelo"] = global_skill_list["gelo"]
                    choosingskill = False

                if choice == "wind":
                    newchar.slist["gale"] = global_skill_list["gale"]
                    choosingskill = False

                if choice == "earth":
                    newchar.slist["tera"] = global_skill_list["tera"]
                    choosingskill = False

                if choice == "thunder":
                    newchar.slist["volt"] = global_skill_list["volt"]
                    choosingskill = False

                if choice == "toxic":
                    newchar.slist["veno"] = global_skill_list["veno"]
                    choosingskill = False

            newchar.slist["enhate"] = global_skill_list["enhate"]
            newchar.slist["enfete"] = global_skill_list["enfete"]
            
        if newchar.char_class == thaumaturge:
            
            choosingskill = True
            while choosingskill:
                os.system("cls")
                print (f"\nElements: Wind, Earth, Thunder")
                choice = input(f"What element is {newchar.name} attuned to?  ").lower()

                if choice == "wind":
                    newchar.slist["gale"] = global_skill_list["gale"]
                    choosingskill = False

                if choice == "earth":
                    newchar.slist["tera"] = global_skill_list["tera"]
                    choosingskill = False

                if choice == "thunder":
                    newchar.slist["volt"] = global_skill_list["volt"]
                    choosingskill = False

            newchar.slist["cura"] = global_skill_list["cura"]
            newchar.slist["revita"] = global_skill_list["revita"]
            
        if newchar.char_class == herald:
            choosingskill = True
            while choosingskill:
                os.system("cls")
                print (f"\nElements: Fire, Ice, Wind, Thunder")
                choice = input(f"What element is {newchar.name} attuned to?  ").lower()

                if choice == "fire":
                    newchar.slist["firo"] = global_skill_list["firo"]
                    choosingskill = False

                if choice == "ice":
                    newchar.slist["gelo"] = global_skill_list["gelo"]
                    choosingskill = False

                if choice == "wind":
                    newchar.slist["gale"] = global_skill_list["gale"]
                    choosingskill = False

                if choice == "earth":
                    newchar.slist["tera"] = global_skill_list["tera"]
                    choosingskill = False

                if choice == "thunder":
                    newchar.slist["volt"] = global_skill_list["volt"]
                    choosingskill = False

            newchar.slist["cura"] = global_skill_list["cura"]
            newchar.slist["enhast"] = global_skill_list["enhast"]

        if newchar.char_class == knight:

            newchar.slist["charge"] = global_skill_list["charge"]
            newchar.slist["cleave"] = global_skill_list["cleave"]
            newchar.slist["protect"] = global_skill_list["protect"]

        if newchar.char_class == scout:
            newchar.slist["sneak"] = global_skill_list["sneak"]
            newchar.slist["hunt"] = global_skill_list["hunt"]
            newchar.slist["decoy"] = global_skill_list["decoy"]

        if newchar.char_class == quartermaster:
            newchar.slist["coating"] = global_skill_list["coating"]
            newchar.slist["appraise"] = global_skill_list["appraise"]
            newchar.slist["bomb"] = global_skill_list["bomb"]

        pass

    print (f"\n{newchar.name}, {newchar.race.name} {newchar.char_class.name}")
    print (f"  HP : {newchar.hp} / TP : {newchar.tp}\n  STR: {newchar.str} (DMG: {newchar.dmg}) / TEC: {newchar.tec} / VIT: {newchar.vit} / AGI: {newchar.agi} / LCK: {newchar.lck}")
    print ("Skills:")
    for n in newchar.slist:
        print (f" {n.upper()}, Skill Level {newchar.slist[n][0]}")

    # Equip bonus
    newchar.str += 1
    newchar.vit += 1
    newchar.agi += 1

    choice_final = input ("\nIs this the character you want? (type 'no' to cancel)  ")

    if choice_final in cancelterms:
        return None
    else:
        character_roster.append(copy.deepcopy(newchar))
        input(f"Character {newchar.name} has been added to the roster. Type anything to continue.  ")
        return newchar
    pass

def checkRoster():
    global party_money
    checkingroster = True

    while checkingroster:
        os.system("cls")
        print ("ROSTER")
        for index, char in enumerate(character_roster):
            print (f"({character_roster.index(char)}) {char.name}: a {char.race.name} {char.char_class.name}.")

        print ("\nPARTY")
        for index, char in enumerate(party):
            print (f"({party.index(char)}) {char.name}: a {char.race.name} {char.char_class.name}.")

        choice = input("\nDo you want to (I)nspect a character, (D)ismiss a Vagranteer, (A)dd or (R)emove from party, (T)rain Perks, or (Q)uit?").lower()

        if choice == "":
            pass

        elif choice in ("d"):
            choice_roster = input("What character do you want to permanently remove from the Roster?")

            try:
                choice_roster = int(choice_roster)
            except ValueError:
                choice_roster = None

            if choice_roster is not None:
                if choice_roster in range (len(character_roster)):
                    char = character_roster[choice_roster]
                    choice = input (f"This will PERMANENTLY remove {char.name} from the Roster. They will be lost forever.\nDo you want to continue? Y/N  ")

                    if choice in ("y"):
                        if char.hp > 0:
                            party_money += char.level*5
                            print(f"{char.name} part ways. They leave behind {char.level*5} Cr as a token of good-will.")
                        else:
                            print(f"{char.name}'s body is sent back to their family.")

                        character_roster.remove(character_roster[choice_roster])

        elif choice in ("i"):

            choice_type = input("(R)oster or (P)arty?  ").lower()

            if choice_type in ("r"):

                choice_roster = input("Which character from the Roster?")

                try:
                    choice_roster = int(choice_roster)
                except ValueError:
                    choice_roster = None

                if choice_roster is not None:
                    if int(choice_roster) in range (len(character_roster)):

                        char = character_roster[int(choice_roster)]

                        print(f"\n{char.name}'s Status\n Race: {char.race.name} / Class: {char.char_class.name} / Level: {char.level} ({round(char.exp)} / {round(char.level*1000)} EXP)\n HP: {math.floor(char.hp)} / {math.floor(char.maxhp)} // TP: {math.floor(char.tp)} / {math.floor(char.maxtp)}\n STR: {math.floor(char.str)} (DMG: {int(char.dmg)}) / TEC: {math.floor(char.tec)} / VIT: {math.floor(char.vit)} / AGI: {math.floor(char.agi)} / LCK: {math.floor(char.lck)}")
                        from CombatSystem import fetchSkills
                        fetchSkills(char)
                        input ("Press anything to continue.")
            
            elif choice_type in ("p"):

                choice_party = input("Which character from the Party?")

                try:
                    choice_party = int(choice_party)
                except ValueError:
                    choice_party = None

                if choice_party is not None:
                    if int(choice_party) in range (len(party)):

                        char = party[choice_party]

                        print(f"\n{char.name}'s Status\n Race: {char.race.name} / Class: {char.char_class.name} / Level: {char.level} ({round(char.exp)} / {round(char.level*1000)} EXP)\n HP: {math.floor(char.hp)} / {math.floor(char.maxhp)} // TP: {math.floor(char.tp)} / {math.floor(char.maxtp)}\n STR: {math.floor(char.str)} (DMG: {int(char.dmg)}) / TEC: {math.floor(char.tec)} / VIT: {math.floor(char.vit)} / AGI: {math.floor(char.agi)} / LCK: {math.floor(char.lck)}")
                        from CombatSystem import fetchSkills
                        fetchSkills(char)
                        input ("Press anything to continue.")

        elif choice in ("a"):
            choice_roster = None
            if len(party) >= 4:
                print("The party is full already. Please remove vagranteers before adding more.")
                input ("Press anything to continue")
            else:
                choice_roster = input("Add which character from the Roster?")

                try:
                    choice_roster = int(choice_roster)
                except ValueError:
                    choice_roster = None


                if choice_roster is not None:
                    party.append(character_roster[choice_roster])
                    character_roster.remove(character_roster[choice_roster])

        elif choice in ("r"):
            choice_party = None
            if len(party) < 1:
                print("The party is empty.")
                input ("Press anything to continue")
            else:
                choice_party = input("Remove which character from the Party?")

                try:
                    choice_party = int(choice_party)
                except ValueError:
                    choice_party = None


                if choice_party is not None:
                    character_roster.append(party[choice_party])
                    party.remove(party[choice_party])


        elif choice in ("t"):
            
            managePerks()

        elif choice in ("q"):
            if len(party) <= 0:
                input ("Party can't be empty. Press anything to continue.")
            elif len(party) >= 1:
                checkingroster = False

def runRoster():
    testing_characters = True

    while testing_characters:
        
        print (f"\nThere are {len(character_roster)} characters in the roster.")

        command = input(f"What do you want to do?\n Create a (N)ew Character, check the (R)oster, or (Q)uit?").lower()

        if command in ["r", "roster"]:

            checkRoster()
            
        elif command in ["n","new"]:

            createCharacter()

        elif command in ["q", "quit"]:
            testing_characters = False

def managePerks():
    m_perks = True
    
    while m_perks:
        os.system("cls")
        
        print ("\nPARTY")
        for index, char in enumerate(party):
            print (f"({party.index(char)}) {char.name}: a {char.race.name} {char.char_class.name}.")

        choice_party = None
        choice_party = input("\nManage the Skills/Perks of which Character? (Q)uit to return.  ")

        if choice_party in ("q"):
            m_perks = False

        try:
            choice_party = int(choice_party)
        except ValueError:
            choice_party = None

        if choice_party is not None:
            char = party[choice_party]

            choice = input("Manage (S)kills or (P)erks?").lower()

            if choice == "":
                pass

            elif choice in ("s"):
                if char is not None:
                    print (f"{char.name} has {char.skillpts} skill points and {char.perkpts} perk points.\n")
                    for n in char.slist:
                        print (f"{n.upper()}, Skill Level {char.slist[n][0]} // {char.slist[n][1]}")

                    keys = char.slist.keys()
                    choice = input("What skill you want to inspect and improve? Type the name of skill or (Q) to quit.  ").lower()

                    # try:
                    #     choice = int(choice)
                    # except ValueError:
                    #     choice = None

                    if choice in ("q"):
                        pass

                    elif choice is not None and choice in keys:
                        skill_level = char.slist[choice][0]

                        if choice in ("firo","tera","gelo","gale","veno","volt","nuke"):
                            
                            descriptor = (f"\n{choice.upper()} (Level: {skill_level}) is a skill that causes weak elemental damage.\n")
                            if char.char_class == arcanist:
                                if skill_level <2:
                                    descriptor += (f" At Level 2 you learn GRUN{choice.upper()}, which affects all enemies.\n")
                                if skill_level <3:
                                    descriptor += (f" At Level 3 you learn {choice.upper()}MOR, which causes medium elemental damage.\n")
                                if skill_level <4:
                                    descriptor += (f" At Level 4 you learn GRUN{choice.upper()}MOR, which causes medium elemental damage to all enemies.\n")
                                if skill_level <5:
                                    descriptor += (f" At Level 5 you learn {choice.upper()}MATHA, which causes heavy elemental damage.\n")
                                if skill_level <6:
                                    descriptor += (f" At Level 6 you learn GRUN{choice.upper()}MATHA, which causes heavy elemental damage to all enemies.")
                            elif char.char_class == herald or char.char_class == thaumaturge:
                                if skill_level <3:
                                    descriptor += (f" At Level 3 you learn GRUN{choice.upper()}, which affects all enemies.\n")
                                if skill_level <4:
                                    descriptor += (f" At Level 4 you learn {choice.upper()}MOR, which causes medium elemental damage.\n")
                                if skill_level <6:
                                    descriptor += (f" At Level 6 you learn GRUN{choice.upper()}MOR, which causes medium elemental damage to all enemies.\n")
                                if skill_level <7:
                                    descriptor += (f" At Level 7 you learn {choice.upper()}MATHA, which causes heavy elemental damage.\n")
                                if skill_level <9:
                                    descriptor += (f" At Level 9 you learn GRUN{choice.upper()}MATHA, which causes heavy elemental damage to all enemies.")
                            
                            print (descriptor)
                            choice_final = input("Spend 1 skill point to level up this skill? (Y/N)  ").lower()
                            
                            if choice_final in ("y"):
                                if char.skillpts >0:
                                    char.slist[choice] += 1
                                    char.skillpts -= 1

                                    if char.char_class == arcanist:
                                        if char.slist[choice] >= 2:
                                            char.slist[f"grun{choice.lower()}"] = char.slist[choice]
                                        if char.slist[choice] >= 3:
                                            char.slist[f"{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 4:
                                            char.slist[f"grun{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 5:
                                            char.slist[f"{choice.lower()}matha"] = char.slist[choice]
                                        if char.slist[choice] >= 6:
                                            char.slist[f"grun{choice.lower()}matha"] = char.slist[choice]

                                    elif char.char_class == herald or char.char_class == thaumaturge:
                                        if char.slist[choice] >= 3:
                                            char.slist[f"grun{choice.lower()}"] = char.slist[choice]
                                        if char.slist[choice] >= 4:
                                            char.slist[f"{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 6:
                                            char.slist[f"grun{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 7:
                                            char.slist[f"{choice.lower()}matha"] = char.slist[choice]
                                        if char.slist[choice] >= 9:
                                            char.slist[f"grun{choice.lower()}matha"] = char.slist[choice]
                                    pass
                                else:
                                    input ("You don't have enough skill points. Press anything to continue")
                            else:
                                pass


                        if choice in ("cura"):
                            
                            descriptor = (f"\n{choice.upper()} (Level: {skill_level}) is a skill that heals a light amount of damage.\n")
                            
                            if char.char_class == thaumaturge:
                                if skill_level <2:
                                    descriptor += (f" At Level 2 you learn GRUN{choice.upper()}, which affects all allies.\n")
                                if skill_level <3:
                                    descriptor += (f" At Level 3 you learn {choice.upper()}MOR, which heals a medium amount of damage.\n")
                                if skill_level <4:
                                    descriptor += (f" At Level 4 you learn GRUN{choice.upper()}MOR, which heals a medium amount of damage to all allies.\n")
                                if skill_level <5:
                                    descriptor += (f" At Level 5 you learn {choice.upper()}MATHA, which heals a heavy amount of damage.\n")
                                if skill_level <6:
                                    descriptor += (f" At Level 6 you learn GRUN{choice.upper()}MATHA, which heals a heavy amount of damage to all allies.")
                            elif char.char_class == herald:
                                if skill_level <3:
                                    descriptor += (f" At Level 3 you learn GRUN{choice.upper()}, which affects all allies.\n")
                                if skill_level <4:
                                    descriptor += (f" At Level 4 you learn {choice.upper()}MOR, which heals a medium amount of damage.\n")
                                if skill_level <6:
                                    descriptor += (f" At Level 6 you learn GRUN{choice.upper()}MOR, which heals a medium amount of damage to all allies.\n")
                                if skill_level <7:
                                    descriptor += (f" At Level 7 you learn {choice.upper()}MATHA, which heals a heavy amount of damage.\n")
                                if skill_level <9:
                                    descriptor += (f" At Level 9 you learn GRUN{choice.upper()}MATHA, which heals a heavy amount of damage to all allies.")
                            
                            print (descriptor)
                            choice_final = input("Spend 1 skill point to level up this skill? (Y/N)  ").lower()
                            
                            if choice_final in ("y"):
                                if char.skillpts >0:
                                    char.slist[choice] += 1
                                    char.skillpts -= 1

                                    if char.char_class == arcanist:
                                        if char.slist[choice] >= 2:
                                            char.slist[f"grun{choice.lower()}"] = char.slist[choice]
                                        if char.slist[choice] >= 3:
                                            char.slist[f"{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 4:
                                            char.slist[f"grun{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 5:
                                            char.slist[f"{choice.lower()}matha"] = char.slist[choice]
                                        if char.slist[choice] >= 6:
                                            char.slist[f"grun{choice.lower()}matha"] = char.slist[choice]

                                    elif char.char_class == herald:
                                        if char.slist[choice] >= 3:
                                            char.slist[f"grun{choice.lower()}"] = char.slist[choice]
                                        if char.slist[choice] >= 4:
                                            char.slist[f"{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 6:
                                            char.slist[f"grun{choice.lower()}mor"] = char.slist[choice]
                                        if char.slist[choice] >= 7:
                                            char.slist[f"{choice.lower()}matha"] = char.slist[choice]
                                        if char.slist[choice] >= 9:
                                            char.slist[f"grun{choice.lower()}matha"] = char.slist[choice]
                                    pass
                                else:
                                    input ("You don't have enough skill points. Press anything to continue")

                        # if skill in ("enha","enfe","revita"):

            elif choice in ("p"):
                if char.perkpts <= 0:
                    input ("You have no Perk points to spend. Type anything to continue. ")
        
            pass


# TESTING
# runRoster()


####