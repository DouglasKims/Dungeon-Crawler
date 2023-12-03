#Enemy Generator

#Generating 3 Mallas per level

import copy
import random


class Enemy():
    def __init__(self,name,level,hp,tp,str,dmg,tec,vit,agi,lck):
        self.name = name
        self.level = level
        self.hp = hp
        self.tp = tp
        self.str = str
        self.dmg = dmg
        self.tec = tec
        self.vit = vit
        self.agi = agi
        self.lck = lck

Malla = Enemy(
    name = "Malla", level = 1, hp = 80, tp = 10,
    str = random.randint(2,6), dmg = 1, tec = random.randint(1,4), vit = random.randint(3,12), agi = random.randint(3,9), lck = random.randint(3,9)
    )

enemylist = []

def generateMalla(leveltogen):

    new = copy.deepcopy(Malla)

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

    new.name += f" Malla"
    new.level = 1 + leveltogen
    new.hp = round (80 * (random.random()/2 + 0.75))
    new.hp += round (leveltogen * (80 * (random.random()/2 + 0.75)) * 0.25)

    new.tp = 10 + (10 * leveltogen)
    new.str = random.randint(2,6) + (leveltogen * random.randint(1,4))
    new.dmg = 1 + (leveltogen * 1/4)
    new.tec = random.randint(1,4) + (leveltogen * random.randint(1,4))
    new.vit = random.randint(3,12) + (leveltogen * random.randint(1,6))
    new.agi = random.randint(3,9) + (leveltogen * random.randint(1,4))
    new.lck = random.randint(3,9) + (leveltogen * random.randint(1,4))

    enemylist.append(new)


gen_times = input ("How many Malla to generate? ")
gen_levels = input ("Up to which level? ")

for n in range(int(gen_levels)):
    for _ in range(int(gen_times)):
        generateMalla(n)

for n in enemylist:
    print(f"Level {n.level} {n.name} // HP: {n.hp} / TP: {n.tp} // STR: {n.str} (DMG: {int(n.dmg)}) / TEC: {n.tec} / VIT: {n.vit} / AGI: {n.agi} / LCK: {n.lck}")