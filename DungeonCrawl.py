# Coordinates X,Y for dungeon
# Each coordinate has; "image" to display and allowed movement
# Movement is based on facing; N/S/W/E/ Forwards/Backwards/Left/Right/Turn L/R

# Define dungeon level 1
# Define each coordinate with a type
# Type N="subtype",S="",W="",E=""; subtypes (open,wall,door,etc.)
# (open allows movement, wall forbids move, door allows w/ interaction)

# Define commands (turning and facing)


import os
import random
import time
import copy
import EquipmentSystem
import CombatSystem

# Dungeon Tiles
    # tt101 = r"""
    # \         /
    #  \ _ _ _ / 
    # """

    # tb101 = r"""
    #  /       \
    # /         \
    # """

    # tm101 = r"""
    #   \ _ _ /
    #    |   |
    #    |_ _|
    #   /_ _ _\
    # """

    # t101 = r"""
    #  \ _ _ _ /
    #   |     | 
    #   |     | 
    #   |     |
    #  /       \
    # """
    # t011 = r"""
    #  _ _ _ _ /
    #   |     | 
    #   |     | 
    #  _|_ _ _|
    #          \
    # """

    # t110 = r"""
    #  \ _ _ _ _
    #   |     | 
    #   |     | 
    #   |_ _ _|_
    #  /        
    # """
    # t010 = r"""
    #  _ _ _ _ _
    #   |     | 
    #   |     | 
    #  _|_ _ _|_
            
    # """
    # t000 = r"""
    #  _ _ _ _ _
    #   |     | 
    #   |     | 
    #  _|     |_
            
    # """
    # t111 = r"""
    #  \ _ _ _ /
    #   |     | 
    #   |     | 
    #   |_ _ _|
    #  /       \
    # """
    # t001 = r"""
    #  _ _ _ _ /
    #   |     | 
    #   |     | 
    #  _|     |
    #          \
    # """
    # t100 = r"""
    #  \ _ _ _ _
    #   |     | 
    #   |     | 
    #   |     |_
    #  /       
    # """

    # t121 = r"""
    # \ _ _ _ /
    #  |  _  | 
    #  | | | | 
    #  | | | |
    # /       \
    # """



# Subtypes Open(0),Wall(1),Door(2),L.Door(D),Secret Wall(9)
# Subtypes2: (C)hest, (O)penChest, Stairs(U)p, Stairs (D)own, (R)esting Area, (M)erchant,
# SubtypesD: Secret walls accessible only by (N)(S)(W)(E)
class Tile:
    def __init__(self,name,N,W,E,S,seen):
        self.name = name
        self.N = N
        self.W = W
        self.E = E
        self.S = S
        self.seen = seen

C = "C" # Chest
O = "O" # Open Chest
U = "U" # Stairs Up
D = "D" # Stairs Down
N = "N" # Secret passage north only
S = "S" # Secret Passage South only
W = "W" # Secret Passage West only
E = "E" # Secret Passage East only
R = "R" # Resting Area
M = "M" # Merchant

dungeon01 = [[Tile('1100',1,1,0,0,False),Tile('1010',1,0,1,0,False),Tile('1110',1,1,1,0,False)],
             [Tile('0110',0,1,1,0,False),Tile('0110',0,1,1,0,False),Tile('0110',0,1,1,0,False)],
             [Tile('0111',0,1,1,1,False),Tile('0101',0,1,0,1,False),Tile('0011',0,0,1,1,False)],
             ]


testdungeon = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,2,0,0,0,1],
    [1,0,1,1,9,1,0,1,0,1],
    [1,0,1,0,0,1,0,1,0,1],
    [1,2,1,0,1,1,0,0,0,1],
    [1,0,1,0,1,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,D,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
]




dungeon11 = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],

    [1,U,0,0,1,0,C,1,1,1,0,E,0,0,0,0,0,1,0,0,0,0,0,1,0,1,0,0,0,0,0,1], #1
    [1,0,0,0,2,0,0,1,C,0,0,1,0,1,0,1,0,1,0,1,1,1,0,0,0,0,0,1,0,0,0,1], #2
    [1,0,0,0,1,0,0,1,1,1,0,1,0,1,1,1,0,0,0,0,0,1,1,1,1,0,1,1,0,0,0,1], #3
    [1,1,1,1,1,0,0,E,0,0,0,1,0,1,0,1,0,1,0,1,0,0,1,0,1,0,1,0,0,1,1,1], #4
    [1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,0,1,0,1,1,0,1,0,0,0,1,0,0,1,C,1], #5

    [1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,0,1,0,0,1,0,1,0,1,1,1,0,1,1,0,1],
    [1,0,0,1,0,0,0,1,0,1,1,1,1,2,1,1,1,1,0,C,1,0,1,1,1,0,1,0,1,1,0,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,0,0,M,1,1,1,1,1,1,0,1,0,1,0,1,0,W,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,2,0,R,0,2,0,0,0,0,0,0,1,0,0,0,1,0,1,1,1,1],
    [1,1,1,1,0,1,0,1,0,1,1,1,0,0,0,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,0,1], #10

    [1,0,0,0,0,1,0,1,0,0,0,1,1,2,1,1,C,1,0,0,0,1,1,0,1,1,1,1,1,1,0,1],
    [1,0,1,1,0,1,0,1,1,1,0,1,0,0,1,C,0,0,0,0,0,1,0,0,0,0,0,0,C,1,0,1],
    [1,0,C,1,0,0,0,1,0,0,0,1,0,1,1,1,C,1,0,1,1,1,0,1,1,1,1,1,1,1,0,1],
    [1,0,1,1,0,1,0,1,1,1,1,1,0,1,C,1,1,1,0,1,0,0,0,1,0,0,0,0,0,0,0,1],
    [1,0,0,0,0,1,0,1,0,C,0,1,0,1,0,0,0,0,0,1,0,1,0,1,0,1,1,1,1,1,1,1], #15

    [1,1,1,1,1,1,S,1,0,0,0,1,0,1,1,1,1,1,2,1,2,1,1,1,0,1,C,0,0,2,0,1],
    [1,0,0,0,0,0,0,1,1,0,1,1,0,1,0,0,0,2,0,0,0,2,0,0,0,1,C,0,0,1,0,1],
    [1,0,1,1,1,1,0,0,0,0,0,0,0,1,0,1,1,1,0,R,0,1,1,1,0,1,C,0,0,1,2,1],
    [1,0,0,0,0,1,1,1,1,0,1,1,0,1,0,1,0,2,0,0,0,2,0,1,0,1,1,1,1,1,0,1],
    [1,0,1,1,0,0,0,0,1,2,1,0,0,1,C,1,0,1,2,1,2,1,0,1,0,0,0,0,0,1,0,1], #20

    [1,0,0,1,1,1,1,2,1,0,1,0,1,1,1,1,0,1,0,1,0,1,0,1,1,1,1,1,0,0,0,1],
    [1,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,0,1,0,1,0,1,0,1,0,0,C,1,1,1,1,1],
    [1,1,0,1,1,0,1,1,0,0,1,1,1,1,1,1,1,1,0,1,0,1,0,0,0,1,1,1,0,0,0,1],
    [1,1,0,0,1,0,0,0,0,1,0,0,0,1,0,0,0,0,0,1,0,1,1,1,0,C,1,0,0,1,0,1],
    [1,0,0,1,1,1,1,1,S,0,1,1,0,1,0,1,1,S,1,1,0,0,0,1,C,1,1,0,1,1,0,1], #25

    [1,0,0,1,C,1,0,0,0,0,0,1,0,1,0,1,M,0,0,1,1,1,0,1,1,1,0,0,1,0,0,1],
    [1,0,1,1,0,1,0,1,0,1,0,1,0,1,0,1,0,R,0,2,0,1,0,1,0,0,0,1,1,2,1,1],
    [1,0,1,0,0,1,0,1,C,1,0,1,0,0,0,1,0,0,0,1,0,1,0,0,0,1,1,1,0,0,0,1],
    [1,0,1,0,0,1,0,1,1,1,0,1,1,1,1,1,1,2,1,1,0,1,1,1,1,1,0,2,0,0,0,1],
    [1,0,0,0,0,1,0,0,0,0,0,2,0,0,0,0,0,0,1,1,0,0,0,0,0,0,0,1,0,0,D,1], #30
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1]
]

item1 = EquipmentSystem.item1
item2 = EquipmentSystem.item2
item3 = EquipmentSystem.item3
access2 = EquipmentSystem.access2
armor1 = EquipmentSystem.armor1
armor2 = EquipmentSystem.armor2
weapon1 = EquipmentSystem.weapon1
weapon2 = EquipmentSystem.weapon2

dungeon11loot = {
    "1,6": (item1, 1,6),
    "2,8": (item1 ,2,8),
    "13,2": (item2 ,13,2),
    "26,4": (armor1 ,26,4),
    "14,9": (armor2 ,14,9),
    "28,8": (weapon2 ,28,8),
    "14,14": (item3 ,14,14),
    "20,14": (access2 ,20,14),
    "11,16": (item1 ,11,16),
    "12,15": (item2 ,12,15),
    "13,16": (item2 ,13,16),
    "7,19": (item1 ,7,19),
    "12,28": (weapon1 ,12,28),
    "15,26": (item2 ,15,26),
    "16,26": (item3 ,16,26),
    "17,26": (item1 ,17,26),
    "22,26": (item2 ,22,26),
    "24,25": (item2 ,24,25),
    "25,24": (item2 ,25,24),
}


dungeon11test = [
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
    #0,1,2,3,4,5, , , , ,1, , , , ,5, , , , ,2, , , , ,5, , , , ,3,1
    [1,U,0,0,1,0,C,1,1,1,0,E,0,0,0,0,1], #1
    [1,0,0,0,2,0,0,1,C,0,0,1,0,1,0,1,1], #2
    [1,0,0,0,1,0,0,1,1,1,0,1,0,1,1,1,1], #3
    [1,1,1,1,1,0,0,E,0,0,0,1,0,1,0,1,1], #4
    [1,0,0,0,0,0,0,1,1,1,0,1,0,1,0,1,1], #5

    [1,0,1,1,0,1,1,1,0,0,0,1,0,0,0,0,1],
    [1,0,0,1,0,0,0,1,0,1,1,1,1,2,1,1,1],
    [1,0,1,1,1,1,0,1,0,1,1,1,0,0,M,1,1],
    [1,0,0,0,0,1,0,0,0,0,0,2,0,R,0,2,1],
    [1,1,1,1,0,1,0,1,0,1,1,1,0,0,0,1,1], #10
    [1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1,1],
]


def tileLookup(tiley, tilex, dungeon_bp):

    tile = dungeon_bp[tiley][tilex]

    
    try:
        tn = dungeon_bp[tiley-1][tilex]
    except IndexError:
        tn = 1
    
    try:
        tw = dungeon_bp[tiley][tilex-1]
    except IndexError:
        tw = 1

    try:
        te = dungeon_bp[tiley][tilex+1]
    except IndexError:
        te = 1

    try:
        ts = dungeon_bp[tiley+1][tilex]
    except IndexError:
        ts = 1

    # ts = dungeon_bp[tiley+1][tilex]

    ttype = [tn,tw,te,ts]
    
    if tile == 0:
        for i in range(len(ttype)):
            if ttype[i] != 1: # Isn't Wall?
                if ttype[i] == 0: # Is corridor?
                    ttype[i] = 0
                elif ttype[i] == 2: # Is Door?
                    ttype[i] = 2
                elif ttype[i] == C: # Is Chest?
                    ttype[i] = C
                elif ttype[i] == O: # Is Open Chest?
                    ttype[i] = O
                elif ttype[i] == R: # Is Rest Area?
                    ttype[i] = R
                elif ttype[i] == U: # Is Stairs Up?
                    ttype[i] = U
                elif ttype[i] == D: # Is Stairs Down?
                    ttype[i] = D
                elif ttype[i] == M: # Is Merchant?
                    ttype[i] = M

                elif ttype[i] == N: # Is secret-north?
                    ttype[i] = N
                elif ttype[i] == S: # Is secret-south?
                    ttype[i] = S
                elif ttype[i] == W: # Is Chest-west?
                    ttype[i] = W
                elif ttype[i] == E: # Is Chest-east?
                    ttype[i] = E
            else:
                ttype[i] = 1

    if tile == 1:
        for i in range(len(ttype)):
            ttype[i] = 1

    tiletitle = f"{ttype[0]}{ttype[1]}{ttype[2]}{ttype[3]}"
    finaltile = Tile(tiletitle,ttype[0],ttype[1],ttype[2],ttype[3],False)
    
    return finaltile

dungeon_blueprint = []
def buildDungeon(dungeon_bp,level,lootlist):
    global dungeon_blueprint
    global dungeon_level
    global dungeon_current_loot

    dungeon_level = level
    dungeon_current_loot = lootlist
    dungeon_blueprint = dungeon_bp
    newdungeon = []
    nny = 0
    for ny in range(0, len(dungeon_bp)):
        horizontal = []
        nnx = 0
        for nx in dungeon_bp[ny]:
            # print(f"{nny}, {nnx}")
            horizontal.append(tileLookup(nny,nnx,dungeon_bp))
            nnx += 1
        newdungeon.append(horizontal)
        nny += 1
    
    return newdungeon


# dungeon_current = buildDungeon(testdungeon, 1)
dungeon_current_loot = None
dungeon_current = buildDungeon(dungeon11, 1, dungeon11loot)
# dungeon_current = dungeon01
# print(dungeon_current)

party = CombatSystem.party
party_coord = [2,2]
party_facing = 2
danger = 0
danger_level = ""
dungeon_level = 1
check = dungeon_current[party_coord[0]][party_coord[1]]
vision = None
hour_names = ["Dawn","Morning","Noon","Afternoon","Twilight","Evening","Midnight","Witching Hour"]
# Dark between time = 4*90 and time = 7*90 // Each 90 steps advances the clock
hour = 0
steps = 0

#Facings; N=8, S=2, W=4, E=6

#Game Logic
def update_coord(x,y):
    global party_coord
    global check
    party_coord[0] += y
    party_coord[1] += x
    check = dungeon_current[party_coord[0]][party_coord[1]]
    
    update_time()    
    update_seen()
    update_danger()
    

def update_time():
    global steps
    global hour

    steps += 1

    if steps >= 60:
        hour += 1
        steps = 0

    if hour >= 8:
        hour = 0

def update_seen():
    global dungeon_current

    NW = dungeon_current[party_coord[0]+1][party_coord[1]-1]
    N = dungeon_current[party_coord[0]+1][party_coord[1]]
    NE = dungeon_current[party_coord[0]+1][party_coord[1]+1]
    W = dungeon_current[party_coord[0]][party_coord[1]-1]
    C = dungeon_current[party_coord[0]][party_coord[1]]
    E = dungeon_current[party_coord[0]][party_coord[1]+1]
    SW = dungeon_current[party_coord[0]-1][party_coord[1]-1]
    S = dungeon_current[party_coord[0]-1][party_coord[1]]
    SE = dungeon_current[party_coord[0]-1][party_coord[1]+1]

    surrounds = [NW,N,NE,W,C,E,SW,S,SE]

    for n in surrounds:
        n.seen = True

def update_danger():
    global danger
    global danger_level

    danger += random.randint(1,4)

    if danger > 85:
        danger_level = "Red"
    elif danger >50:
        danger_level = "Yellow"
    elif danger > 25:
        danger_level = "Green"
    else:
        danger_level = "None"

# def update_vision():
#     global vision
#     if party_facing == 8:
#         if check.N == 0:
#             front = "Corridor"
#         elif check.N == 1:
#             front = "Wall"
#         elif check.N == 2:
#             front = "Door"

#         if check.W == 0:
#             left = "Corridor"
#         elif check.W == 1:
#             left = "Wall"
#         elif check.W == 2:
#             left = "Door"

#         if check.E == 0:
#             right = "Corridor"
#         elif check.E == 1:
#             right = "Wall"
#         elif check.E == 2:
#             right = "Door"

#     if party_facing == 2:
#         if check.S == 0:
#             front = "Corridor"
#         elif check.S == 1:
#             front = "Wall"
#         elif check.S == 2:
#             front = "Door"

#         if check.E == 0:
#             left = "Corridor"
#         elif check.E == 1:
#             left = "Wall"
#         elif check.E == 2:
#             left = "Door"

#         if check.W == 0:
#             right = "Corridor"
#         elif check.W == 1:
#             right = "Wall"
#         elif check.W == 2:
#             right = "Door"

#     if party_facing == 4:
#         if check.W == 0:
#             front = "Corridor"
#         elif check.W == 1:
#             front = "Wall"
#         elif check.W == 2:
#             front = "Door"

#         if check.S == 0:
#             left = "Corridor"
#         elif check.S == 1:
#             left = "Wall"
#         elif check.S == 2:
#             left = "Door"

#         if check.N == 0:
#             right = "Corridor"
#         elif check.N == 1:
#             right = "Wall"
#         elif check.N == 2:
#             right = "Door"

#     if party_facing == 6:
#         if check.E == 0:
#             front = "Corridor"
#         elif check.E == 1:
#             front = "Wall"
#         elif check.E == 2:
#             front = "Door"

#         if check.N == 0:
#             left = "Corridor"
#         elif check.N == 1:
#             left = "Wall"
#         elif check.N == 2:
#             left = "Door"

#         if check.S == 0:
#             right = "Corridor"
#         elif check.S == 1:
#             right = "Wall"
#         elif check.S == 2:
#             right = "Door"

#     vision = f"you can see a {front} in front of you, a {left} to your left, and a {right} to your right."
#     print (vision)

# def update_picture():
#     if party_facing == 8:
#         if check.W == 0 and check.N == 0 and check.E == 0:
#             print(t000)
#         elif check.W == 1 and check.N == 0 and check.E == 1:
#             print(t101)
#         elif check.W == 0 and check.N == 1 and check.E == 1:
#             print(t011)
#         elif check.W == 1 and check.N == 1 and check.E == 0:
#             print(t110)
#         elif check.W == 0 and check.N == 1 and check.E == 0:
#             print(t010)
#         elif check.W == 1 and check.N == 1 and check.E == 1:
#             print(t111)
#         elif check.W == 0 and check.N == 0 and check.E == 1:
#             print(t001)
#         elif check.W == 1 and check.N == 0 and check.E == 0:
#             print(t100)

#     elif party_facing == 4:
#         if check.S == 0 and check.W == 0 and check.N == 0:
#             print(t000)
#         elif check.S == 1 and check.W == 0 and check.N == 1:
#             print(t101)
#         elif check.S == 0 and check.W == 1 and check.N == 1:
#             print(t011)
#         elif check.S == 1 and check.W == 1 and check.N == 0:
#             print(t110)
#         elif check.S == 0 and check.W == 1 and check.N == 0:
#             print(t010)
#         elif check.S == 1 and check.W == 1 and check.N == 1:
#             print(t111)
#         elif check.S == 1 and check.W == 0 and check.N == 0:
#             print(t100)
#         elif check.S == 0 and check.W == 0 and check.N == 1:
#             print(t001)

#     elif party_facing == 2:
#         if check.E == 0 and check.S == 0 and check.W == 0:
#             print(t000)
#         elif check.E == 1 and check.S == 0 and check.W == 1:
#             print(t101)
#         elif check.E == 0 and check.S == 1 and check.W == 1:
#             print(t011)
#         elif check.E == 1 and check.S == 1 and check.W == 0:
#             print(t110)
#         elif check.E == 0 and check.S == 1 and check.W == 0:
#             print(t010)
#         elif check.E == 1 and check.S == 1 and check.W == 1:
#             print(t111)
#         elif check.E == 1 and check.S == 0 and check.W == 0:
#             print(t100)
#         elif check.E == 0 and check.S == 0 and check.W == 1:
#             print(t001)
        
#     elif party_facing ==6:
#         if check.N == 0 and check.E == 0 and check.S == 0:
#             print(t000)
#         elif check.N == 1 and check.E == 0 and check.S == 1:
#             print(t101)
#         elif check.N == 0 and check.E == 1 and check.S == 1:
#             print(t011)
#         elif check.N == 1 and check.E == 1 and check.S == 0:
#             print(t110)
#         elif check.N == 0 and check.E == 1 and check.S == 0:
#             print(t010)
#         elif check.N == 1 and check.E == 1 and check.S == 1:
#             print(t111)
#         elif check.N == 1 and check.E == 0 and check.S == 0:
#             print(t100)
#         elif check.N == 0 and check.E == 0 and check.S == 1:
#             print(t001)

def getMap():

    global dungeon_blueprint
    localmap = [
        [' ','5',' '],
        ['5','0','5'],
        [' ','5',' '],
        ]
    
    localmaplight = [
        [' ',' ',' ',' ',' '],
        [' ',' ','5',' ',' '],
        [' ','5','0','5',' '],
        [' ',' ','5',' ',' '],
        [' ',' ',' ',' ',' ']
        ]
    
    map_coords = {
        "NW": (dungeon_blueprint[party_coord[0]-1][party_coord[1]-1], 0, 0),
        "N" : (dungeon_blueprint[party_coord[0]-1][party_coord[1]], 0, 1),
        "NE" : (dungeon_blueprint[party_coord[0]-1][party_coord[1]+1], 0, 2),
        "W": (dungeon_blueprint[party_coord[0]][party_coord[1]-1], 1, 0),
        "E" : (dungeon_blueprint[party_coord[0]][party_coord[1]+1], 1, 2),
        "SW": (dungeon_blueprint[party_coord[0]+1][party_coord[1]-1], 2, 0),
        "S" : (dungeon_blueprint[party_coord[0]+1][party_coord[1]], 2, 1),
        "SE" : (dungeon_blueprint[party_coord[0]+1][party_coord[1]+1], 2, 2)
    }

    map_coords_bright = {}
    
    # Adding map coordinates to bright map
    try:
        for iy in range(-2, 3):
            for jx in range(-2, 3):
                if iy != 0 or jx != 0:
                    map_coords_bright[f"{iy+2},{jx+2}"] = (dungeon_blueprint[party_coord[0]+iy][party_coord[1]+jx], iy+2, jx+2)
    except IndexError:
        map_coords_bright[f"{iy+2},{jx+2}"] = (None, iy, jx)

    map_coords_bright["NW"]=(dungeon_blueprint[party_coord[0]-1][party_coord[1]-1], 1, 1)
    map_coords_bright["N"]=(dungeon_blueprint[party_coord[0]-1][party_coord[1]], 1, 2)
    map_coords_bright["NE"]=(dungeon_blueprint[party_coord[0]-1][party_coord[1]+1], 1, 3)
    map_coords_bright["W"]=(dungeon_blueprint[party_coord[0]][party_coord[1]-1], 2, 1)
    map_coords_bright["E"]=(dungeon_blueprint[party_coord[0]][party_coord[1]+1], 2, 3)
    map_coords_bright["SW"]=(dungeon_blueprint[party_coord[0]+1][party_coord[1]-1], 3, 1)
    map_coords_bright["S"]=(dungeon_blueprint[party_coord[0]+1][party_coord[1]], 3, 2)
    map_coords_bright["SE"]=(dungeon_blueprint[party_coord[0]+1][party_coord[1]+1], 3, 3)

    
    #Check visibility map bright
    if map_coords_bright["NW"][0] != 0:
         map_coords_bright["0,0"]=(None, 0, 0)
         map_coords_bright["0,1"]=(None, 0, 1)
         map_coords_bright["1,0"]=(None, 1, 0)
    if map_coords_bright["NE"][0] != 0:
         map_coords_bright["0,3"]=(None, 0, 3)
         map_coords_bright["0,4"]=(None, 0, 4)
         map_coords_bright["1,4"]=(None, 1, 4)
    if map_coords_bright["SW"][0] != 0:
         map_coords_bright["3,0"]=(None, 3, 0)
         map_coords_bright["4,0"]=(None, 4, 0)
         map_coords_bright["4,1"]=(None, 4, 1)
    if map_coords_bright["SE"][0] != 0:
         map_coords_bright["4,4"]=(None, 4, 4)
         map_coords_bright["3,4"]=(None, 3, 4)
         map_coords_bright["4,3"]=(None, 4, 3)

    if map_coords_bright["N"][0] != 0:
        map_coords_bright["0,2"]=(None, 0, 2)
    if map_coords_bright["W"][0] != 0:
        map_coords_bright["2,0"]=(None, 2, 0)
    if map_coords_bright["E"][0] != 0:
        map_coords_bright["2,4"]=(None, 2, 4)
    if map_coords_bright["S"][0] != 0:
        map_coords_bright["4,2"]=(None, 4, 2)
    
    if party_facing == 8:
        localmap[1][1] = "▲"
        map_coords["SW"]=(None, 2, 0)
        map_coords["S"]=(None, 2, 1)
        map_coords["SE"]=(None, 2, 2)

        localmaplight[2][2] = "▲"
        map_coords_bright["S"]=(None, 3, 2)
        map_coords_bright["4,3"]=(None, 4, 3)
        map_coords_bright["4,2"]=(None, 4, 2)
        map_coords_bright["4,1"]=(None, 4, 1)

    elif party_facing == 2:
        localmap[1][1] = "▼"
        map_coords["NW"]=(None, 0, 0)
        map_coords["N"]=(None, 0, 1)
        map_coords["NE"]=(None, 0, 2)

        localmaplight[2][2] = "▼"
        map_coords_bright["N"]=(None, 1, 2)
        map_coords_bright["0,3"]=(None, 0, 3)
        map_coords_bright["0,2"]=(None, 0, 2)
        map_coords_bright["0,1"]=(None, 0, 1)

    elif party_facing == 4:
        localmap[1][1] = "◄"
        map_coords["NE"]=(None, 0, 2)
        map_coords["E"]=(None, 1, 2)
        map_coords["SE"]=(None, 2, 2)

        localmaplight[2][2] = "◄"
        map_coords_bright["E"]=(None, 2, 3)
        map_coords_bright["1,4"]=(None, 1, 4)
        map_coords_bright["2,4"]=(None, 2, 4)
        map_coords_bright["3,4"]=(None, 3, 4)
    
    
    elif party_facing == 6:
        localmap[1][1] = "►"
        map_coords["NW"]=(None, 0, 0)
        map_coords["W"]=(None, 1, 0)
        map_coords["SW"]=(None, 2, 0)

        localmaplight[2][2] = "►"
        map_coords_bright["W"]=(None, 2, 1)
        map_coords_bright["1,0"]=(None, 1, 0)
        map_coords_bright["2,0"]=(None, 2, 0)
        map_coords_bright["3,0"]=(None, 3, 0)
    
    for key, values in map_coords.items():
        t, y, x = values
        if t == 0:
            localmap[y][x] = ' '
        elif t == 1 or t == 9:
            localmap[y][x] = '■'
        elif t == 2 or t == 3:
            localmap[y][x] = '□'
        elif t == "U" or t == "D":
            localmap[y][x] = '♦'
        elif t == "C":
            localmap[y][x] = '●'
        elif t == "O":
            localmap[y][x] = '○'
        elif t == "R":
            localmap[y][x] = '♥'
        elif t == "M":
            localmap[y][x] = '☺'
        elif t == "S":
            localmap[y][x] = '↑'
        elif t == "N":
            localmap[y][x] = '↓'
        elif t == "W":
            localmap[y][x] = '→'
        elif t == "E":
            localmap[y][x] = '←'

    for key, values in map_coords_bright.items():
        t, y, x = values
        if t == 0:
            localmaplight[y][x] = ' '
        elif t == 1 or t == 9:
            localmaplight[y][x] = '■'
        elif t == 2 or t == 3:
            localmaplight[y][x] = '□'
        elif t == "U" or t == "D":
            localmaplight[y][x] = '♦'
        elif t == "C":
            localmaplight[y][x] = '●'
        elif t == "O":
            localmaplight[y][x] = '○'
        elif t == "R":
            localmaplight[y][x] = '♥'
        elif t == "M":
            localmaplight[y][x] = '☺'
        elif t == "S":
            localmaplight[y][x] = '↑'
        elif t == "N":
            localmaplight[y][x] = '↓'
        elif t == "W":
            localmaplight[y][x] = '→'
        elif t == "E":
            localmaplight[y][x] = '←'
        elif t == None:
            localmaplight[y][x] = 'X'

    


    if hour >= 4:
        for n in range(0,len(localmap)):
            # print(f"{localmap[n]}")
            print(' '.join(localmap[n]))
    else:
        for n in range(0,len(localmaplight)):
            # print(f"{localmap[n]}")
            print(' '.join(localmaplight[n]))


def debugDungeonMap():
    dungeonmap = ''
    for n in range(0,len(dungeon_current)):
        for y in dungeon_current[n]:
            dungeonmap += f" {y.name}"
        dungeonmap += "\n"
    
    print(dungeonmap)
    pass

def dungeonMap():
    global dungeon_blueprint

    dungeon_mapped = "Dungeon Map\n"
    nny = 0
    for ny in range(0, len(dungeon_current)):
        horizontal = ""
        nnx = 0
        for nx in dungeon_current[ny]:
            dungeon_coord = [nny,nnx]
            if dungeon_coord == party_coord:
                if party_facing == 8:
                    horizontal += " ▲ "
                elif party_facing == 2:
                    horizontal += " ▼ "
                elif party_facing == 4:
                    horizontal += " ◄ "
                elif party_facing == 6:
                    horizontal += " ► "
            elif dungeon_current[nny][nnx].seen == True:
                if dungeon_blueprint[nny][nnx] == 0:
                    horizontal += f"   "
                elif dungeon_blueprint[nny][nnx] == 1 or dungeon_blueprint[nny][nnx] == 9:
                    horizontal += f" ■ "
                elif dungeon_blueprint[nny][nnx] == 2 or dungeon_blueprint[nny][nnx] == 3:
                    horizontal += f" □ "
                elif dungeon_blueprint[nny][nnx] == "U" or dungeon_blueprint[nny][nnx] == "D":
                    horizontal += f" ♦ "
                elif dungeon_blueprint[nny][nnx] == "C":
                    horizontal += f' ● '
                elif dungeon_blueprint[nny][nnx] == "O":
                    horizontal += f' ○ '
                elif dungeon_blueprint[nny][nnx] == "R":
                    horizontal += f' ♥ '
                elif dungeon_blueprint[nny][nnx] == "M":
                    horizontal += f' ☺ '
                elif dungeon_blueprint[nny][nnx] == "S":
                    horizontal += f' ↑ '
                elif dungeon_blueprint[nny][nnx] == "N":
                    horizontal += f' ↓ '
                elif dungeon_blueprint[nny][nnx] == "W":
                    horizontal += f' → '
                elif dungeon_blueprint[nny][nnx] == "E":
                    horizontal += f' ← '
                # horizontal += f" {dungeon_blueprint[nny][nnx]} "
            else:
                horizontal += f"   "
            nnx += 1
        dungeon_mapped += f"{horizontal}\n"
        nny += 1

    print (dungeon_mapped)
    pass


def openDoor():
    
    if party_facing == 8:
        door = party_coord[0]-1, party_coord[1]
    elif party_facing == 4:
        door = party_coord[0], party_coord[1]-1
    elif party_facing == 2:
        door = party_coord[0]+1, party_coord[1]
    elif party_facing == 6:
        door = party_coord[0], party_coord[1]+1

    door = dungeon_blueprint[door[0]][door[1]]
    
    if door == 2:
        print("You open the door and go through it.")
        if party_facing == 8:
            update_coord(0,-2)
        elif party_facing == 4:
            update_coord(-2,0)
        elif party_facing == 2:
            update_coord(0,2)
        elif party_facing ==6:
            update_coord(+2,0)
    elif door == D:
        print("The door seems to be locked.")
    elif door == 9:
        choice = input("You find a secret passage in the wall! Go through it? (Y/N) \n")
        if choice.lower() == "y":
            print("You go across the passage.")
            if party_facing == 8:
                update_coord(0,-2)
            elif party_facing == 4:
                update_coord(-2,0)
            elif party_facing == 2:
                update_coord(0,2)
            elif party_facing ==6:
                update_coord(+2,0)
        else:
            print("Nevermind.")

def interact():

    if party_facing == 8:
        object = party_coord[0]-1, party_coord[1]
    elif party_facing == 4:
        object = party_coord[0], party_coord[1]-1
    elif party_facing == 2:
        object = party_coord[0]+1, party_coord[1]
    elif party_facing == 6:
        object = party_coord[0], party_coord[1]+1

    objecttype = dungeon_blueprint[object[0]][object[1]]

    if objecttype == "U":
        input("Do you want to climb back up?")
    
    if objecttype == "D":
        input("Do you want to climb down?")

    if objecttype == "C":
        getLoot(object[0],object[1])

    if objecttype == "O":
        print("There's nothing else here.")

def getLoot(looty,lootx):

    print ("You scavenge for loot.")

    lootcoord = f"{looty},{lootx}"
    
    if lootcoord in dungeon_current_loot:
        lootitem = dungeon_current_loot[lootcoord][0]


    if len(EquipmentSystem.consumables) >10:
        print(f"Found a {lootitem.name}. But the party stash is full.")    
    else:

        EquipmentSystem.consumables.append(copy.deepcopy(lootitem))
        dungeon_blueprint[looty][lootx] = "O"
        dungeon_current_loot.pop(lootcoord)
        print(f"Found a {lootitem.name}. Added to party's stash.")


directions = {
    8: ("N", (0, -1)),
    4: ("W", (-1, 0)),
    6: ("E", (1, 0)),
    2: ("S", (0, 1))
}

#Game Loop
def exploreDungeon():
    global danger
    global party_facing
    exploring = True
    update_coord(0,0)

    while exploring == True:
        
        if party_coord == [50,50]:
            
            print ("Congratulations, you reached the end of the dungeon!")
            exploring = False
            
            break
        if danger >= 100:
            print("Enemies have appeared!")
            input("Time to fight! (Press anything to begin)")
            danger = 0
            CombatSystem.runCombat()
            os.system("cls")

        # if exploring == True:

        print ("Party:") #spacer
        for n in party:
            print (f"{n.name}'s HP: {n.hp}/{n.maxhp} /// FP: {n.fp}/{n.maxfp}")
        print ("") #spacer
        
        getMap()
        # print(party_coord)
        # update_picture()
        # update_vision()

        
        print(f"Danger level is: {danger_level} // It is currently : {hour_names[hour]}")
        command = input(f"\nType W/8 to go Forwards, Q/7 to turn left, and E/9 to turn right:\nYou can also check the (M)ap, (I)nteract (or F), or (O)pen party menu.\n").lower()

        os.system('cls')
        

        if command == "7" or command == "q":
            if party_facing == 8:
                party_facing = 4
            elif party_facing == 4:
                party_facing = 2
            elif party_facing == 2:
                party_facing = 6
            elif party_facing ==6:
                party_facing = 8

        if command == "9" or command == "e":
            if party_facing == 8:
                party_facing = 6
            elif party_facing == 6:
                party_facing = 2
            elif party_facing == 2:
                party_facing = 4
            elif party_facing == 4:
                party_facing = 8

        if command == "8" or command == "w":

            # facing = directions.get(party_facing)
            if party_facing == 8:
                facing = N
                dx = 0
                dy = -1
            elif party_facing == 6:
                facing = E
                dx = 1
                dy = 0
            elif party_facing == 4:
                facing = W
                dx = -1
                dy = 0
            elif party_facing == 2:
                facing = S
                dx = 0
                dy = 1

            if facing is not None:
                if getattr(check, facing) == 0:
                    update_coord(dx,dy)
                elif getattr(check, facing) == 1:
                    print ("You bonk against a wall.\n")
                elif getattr(check, facing) == 2:
                    print ("There is a door in front of you.\n")
                elif getattr(check, facing) == C:
                    print ("There is a closed chest in front of you.\n")
                elif getattr(check, facing) == O:
                    print ("There is a looted chest in front of you.\n")
                elif getattr(check, facing) == U:
                    print ("These are the stairs upwards.\n")
                elif getattr(check, facing) == D:
                    print ("These are the stairs downwards.\n")
                elif getattr(check, facing) == R:
                    print ("This is a resting area, you can camp here.\n")
                elif getattr(check, facing) == M:
                    print ("This person has merchandise to sell.\n")
                elif getattr(check, facing) in (N,S,W,E):
                    print ("This seems like a passageway, but it is blocked.\n")
                

            

            # if getattr(check,facing) == 0:
            #     update_coord(dx,dy)
            # elif check.facing == 1:
            #     print ("You bonk against a wall.")
            # elif check.facing == 2:
            #     print ("There is a door in front of you.")
            # elif check.facing == C:
            #     print ("There is a closed chest in front of you.")
            # elif check.facing == U:
            #     print ("These are the stairs upwards.")
            # elif check.facing == D:
            #     print ("These are the stairs downwards.")
            # elif check.facing == R:
            #     print ("This is a resting area, you can camp here.")
            # elif check.facing == M:
            #     print ("This person has merchandise to sell.")


            # if party_facing == 8:
            #     if check.N == 0:
            #         update_coord(0,1)
            #     elif check.N == 1:
            #         print ("You bonk against a wall.")
            #     elif check.N == 2:
            #         print ("There is a door in front of you.")
            
            # elif party_facing == 6:
            #     if check.E == 0:
            #         update_coord(1,0)
            #     elif check.E == 1:
            #         print ("You bonk against a wall.")
            #     elif check.E == 2:
            #         print ("There is a door in front of you.")

            # elif party_facing == 2:
            #     if check.S == 0:
            #         update_coord(0,-1)
            #     elif check.S == 1:
            #         print ("You bonk against a wall.")
            #     elif check.S == 2:
            #         print ("There is a door in front of you.")

            # elif party_facing == 4:
            #     if check.W == 0:
            #         update_coord(-1,0)
            #     elif check.W == 1:
            #         print ("You bonk against a wall.")
            #     elif check.W == 2:
            #         print ("There is a door in front of you.")

        if command == "5" or command == "f" or command == "i":
            openDoor()
            interact()

        if command.lower() == "debugmap":
            # getMap(party_coord)
            debugDungeonMap()

            input("Type anything to continue:")

        if command.lower() == "map" or command.lower() == "m":
            dungeonMap()

            input("Type anything to continue:")

        if command.lower() == "o":
            EquipmentSystem.runEquipment()
            

# TEST
exploreDungeon()