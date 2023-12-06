#Enemy Generator

#Generating 3 Mallas per level

import copy
import random
import EnemyList
import math

Enemy = EnemyList.Enemy

class EnemyType():
    def __init__(self, name, hp, tp, str, dmg, tec, vit, agi, lck, imphp, imptp, impstr, impdmg, imptec, impvit, impagi, implck):
        self.name = name
        self.hp = hp
        self.tp = tp
        self.str = str
        self.dmg = dmg
        self.tec = tec
        self.vit = vit
        self.agi = agi
        self.lck = lck
        self.imphp = imphp
        self.imptp = imptp
        self.impstr = impstr
        self.impdmg = impdmg
        self.imptec = imptec
        self.impvit = impvit
        self.impagi = impagi
        self.implck = implck


defaultEnemy = Enemy(
    name = "Enemy", level = 1, maxhp=1, hp = 1, tp = 1,
    str = 1, dmg = 1, tec = 1, vit = 1, agi = 1, lck = 1,
    defending=False,weak=[],resist=[],exp=0,money=0,init=0
    )

enemylist = []

def generateEnemy(type, leveltogen):
    new = copy.deepcopy(defaultEnemy)

    random.seed(None)
    if type == "Malla":
        model = EnemyType(
                name = "Malla",
                hp = round (100 * (random.random()/2 + 0.75)),
                imphp = round((100 * (random.random()/2 + 0.75)) * 0.25),
                tp = 10,
                imptp = 10,
                str = random.randint(2,12),
                impstr = random.randint(1,6),
                tec = random.randint(1,4),
                imptec = random.randint(1,4),
                dmg = 1,
                impdmg = 1/3,
                vit = random.randint(3,12),
                impvit = random.randint(1,6),
                agi = random.randint(3,9),
                impagi = random.randint(1,6),
                lck = random.randint(3,9),
                implck = random.randint(1,6),
                )
        money = random.randint(2,8)

    if type == "Sgeu":
        model = EnemyType(
                name = "Sgeu",
                hp = round (80 * (random.random()/2 + 0.75)),
                imphp = round((80 * (random.random()/2 + 0.75)) * 0.25),
                tp = 10,
                imptp = 10,
                str = random.randint(2,6),
                impstr = random.randint(1,4),
                tec = random.randint(1,4),
                imptec = random.randint(1,4),
                dmg = 1,
                impdmg = 1/4,
                vit = random.randint(3,12),
                impvit = random.randint(1,4),
                agi = random.randint(4,16),
                impagi = random.randint(2,12),
                lck = random.randint(3,18),
                implck = random.randint(1,6)
                )
        money = random.randint(5,15)

    if type == "Diogh":
        model = EnemyType(
                name = "Diogh",
                hp = round (150 * (random.random()/2 + 0.75)),
                imphp = round((150 * (random.random()/2 + 0.75)) * 0.25),
                tp = 10,
                imptp = 10,
                str = random.randint(2,12),
                impstr = random.randint(2,8),
                tec = random.randint(1,4),
                imptec = random.randint(1,4),
                dmg = 2,
                impdmg = 1/2,
                vit = random.randint(2,12),
                impvit = random.randint(1,6),
                agi = random.randint(1,6),
                impagi = random.randint(1,4),
                lck = random.randint(1,6),
                implck = random.randint(1,4)
                )
        money = random.randint(10,20)

    if type == "Colt":
        model = EnemyType(
                name = "Colt",
                hp = round (120 * (random.random()/2 + 0.75)),
                imphp = round((120 * (random.random()/2 + 0.75)) * 0.25),
                tp = 15,
                imptp = 15,
                str = random.randint(2,12),
                impstr = random.randint(1,6),
                tec = random.randint(2,12),
                imptec = random.randint(1,6),
                dmg = 1,
                impdmg = 1/3,
                vit = random.randint(3,12),
                impvit = random.randint(1,6),
                agi = random.randint(2,12),
                impagi = random.randint(1,6),
                lck = random.randint(2,12),
                implck = random.randint(1,6)
                )
        money = random.randint(15,25)

    if type == "Adhbah":
        model = EnemyType(
                name = "Adhbah",
                hp = round (80 * (random.random()/2 + 0.75)),
                imphp = round((80 * (random.random()/2 + 0.75)) * 0.25),
                tp = 20,
                imptp = 15,
                str = random.randint(1,6),
                impstr = random.randint(1,6),
                tec = random.randint(2,8),
                imptec = random.randint(1,8),
                dmg = 1,
                impdmg = 1/5,
                vit = random.randint(2,8),
                impvit = random.randint(1,6),
                agi = random.randint(2,12),
                impagi = random.randint(1,6),
                lck = random.randint(2,12),
                implck = random.randint(1,6)
                )
        money = random.randint(5,15)

    if type == "Grain":
        model = EnemyType(
                name = "Grain",
                hp = round (60 * (random.random()/2 + 0.75)),
                imphp = round((60 * (random.random()/2 + 0.75)) * 0.25),
                tp = 20,
                imptp = 20,
                str = random.randint(1,6),
                impstr = random.randint(1,4),
                tec = random.randint(2,12),
                imptec = random.randint(1,10),
                dmg = 1,
                impdmg = 1/5,
                vit = random.randint(2,8),
                impvit = random.randint(1,6),
                agi = random.randint(2,8),
                impagi = random.randint(1,4),
                lck = random.randint(2,12),
                implck = random.randint(1,6)
                )
        money = random.randint(10,20)

    if type == "Laidir":
        model = EnemyType(
                name = "Laidir",
                hp = round (400 * (random.random()/2 + 0.75)),
                imphp = round((200 * (random.random()/2 + 0.75)) * 0.55),
                tp = 20,
                imptp = 10,
                str = random.randint(15,20),
                impstr = random.randint(5,8),
                tec = random.randint(8,12),
                imptec = random.randint(2,6),
                dmg = 3,
                impdmg = 1/2,
                vit = random.randint(12,15),
                impvit = random.randint(2,8),
                agi = random.randint(6,12),
                impagi = random.randint(1,6),
                lck = random.randint(6,12),
                implck = random.randint(1,6)
                )
        money = random.randint(80,150)

    if leveltogen is not None:
        if leveltogen == 0:
            new.name = f"{random.choice(['Puny','Weak','Cowardly'])}"
        elif leveltogen == 1:
            new.name = f"{random.choice(['Malicious','Insidious','Cruel'])}"
        elif leveltogen == 2:
            new.name = f"{random.choice(['Hateful','Spiteful','Wrathful'])}"
        elif leveltogen == 3:
            new.name = f"{random.choice(['Angry','Merciless','Viscerous'])}"
        elif leveltogen >= 4:
            new.name = f"{random.choice(['Cursed','Divisive','Unpleasant'])}"

    new.name += f" {model.name}"
    new.level = 1 + leveltogen
    new.maxhp = model.hp
    new.maxhp += round(leveltogen * model.imphp)
    new.hp = new.maxhp

    new.tp = model.tp + (model.imptp * leveltogen)
    new.str = model.str + (leveltogen * model.impstr)
    new.dmg = model.dmg + (leveltogen * model.impdmg)
    new.tec = model.tec + (leveltogen * model.imptec)
    new.vit = model.vit + (leveltogen * model.impvit)
    new.agi = model.agi + (leveltogen * model.impagi)
    new.lck = model.lck + (leveltogen * model.implck)
    new.money = money * (leveltogen + 1)

    enemylist.append(new)

    return new

def runGenerator():


    gen_type = input ("What enemy you want to generate?\n (M)alla, (S)geu, (D)iogh, (C)olt, (A)dhbah, (G)rain, (L)àidir, or (R)andom?").lower()
    gen_times = input ("How many enemies to generate? ")
    gen_levels = input ("Up to which level? ")

    if gen_type == "m":
        entype = "Malla"
    elif gen_type == "s":
        entype = "Sgeu"
    elif gen_type == "d":
        entype = "Diogh"
    elif gen_type == "c":
        entype = "Colt"
    elif gen_type == "a":
        entype = "Adhbah"
    elif gen_type == "g":
        entype = "Grain"
    elif gen_type == "r":
        gen_type = "Random"
    elif gen_type == "l":
        entype = "Laidir"


    for n in range(int(gen_levels)):
        for _ in range(int(gen_times)):
            if gen_type == "Random":
                entype = random.choice(["Malla","Sgeu","Diogh","Colt","Adhbah","Grain","Laidir"])
            generateEnemy(entype, n)

    for n in enemylist:
        print(f"Level {n.level} {n.name} // HP: {n.hp} / TP: {n.tp} // STR: {n.str} (DMG: {int(n.dmg)}) / TEC: {n.tec} / VIT: {n.vit} / AGI: {n.agi} / LCK: {n.lck} // DMG pot. PHYS: {round((math.sqrt(n.str)/10+1) * 2.5 * n.str + n.str)} / ELEM: {round((math.sqrt(n.tec)/10+1) * 5 * n.tec)} / Money: {n.money}")

        # dmg = round((math.sqrt(n.str)/10+1) * 2.5 + n.str)



#TEST
# runGenerator()

###