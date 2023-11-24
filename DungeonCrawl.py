# Coordinates X,Y for dungeon
# Each coordinate has; "image" to display and allowed movement
# Movement is based on facing; N/S/W/E/ Forwards/Backwards/Left/Right/Turn L/R

# Define dungeon level 1
# Define each coordinate with a type
# Type N="subtype",S="",W="",E=""; subtypes (open,wall,door,etc.)
# (open allows movement, wall forbids move, door allows w/ interaction)

# Define commands (turning and facing)

#Dungeon Level 1
# _ _ _
#|   | |
#| | | |
#|_|_ _|

import os

#Dungeon Tiles
t101 = r"""
 \ _ _ _ /
  |     | 
  |     | 
  |     |
 /       \
"""
t011 = r"""
 _ _ _ _ /
  |     | 
  |     | 
 _|_ _ _|
         \
"""

t110 = r"""
 \ _ _ _ _
  |     | 
  |     | 
  |_ _ _|_
 /        
"""
t010 = r"""
 _ _ _ _ _
  |     | 
  |     | 
 _|_ _ _|_
          
"""
t000 = r"""
 _ _ _ _ _
  |     | 
  |     | 
 _|     |_
          
"""
t111 = r"""
 \ _ _ _ /
  |     | 
  |     | 
  |_ _ _|
 /       \
"""
t001 = r"""
 _ _ _ _ /
  |     | 
  |     | 
 _|     |
         \
"""
t100 = r"""
 \ _ _ _ _
  |     | 
  |     | 
  |     |_
 /       
"""



# Subtypes Open(0),Wall(1),Door(2)
class Tile:
    def __init__(self,name,N,W,E,S):
        self.name = name
        self.N = N
        self.W = W
        self.E = E
        self.S = S


dungeon01 = [[Tile('1100',1,1,0,0),Tile('1010',1,0,1,0),Tile('1110',1,1,1,0)],
             [Tile('0110',0,1,1,0),Tile('0110',0,1,1,0),Tile('0110',0,1,1,0)],
             [Tile('0111',0,1,1,1),Tile('0101',0,1,0,1),Tile('0011',0,0,1,1)],
             ]

# dungeon01 = [[Tile(0,1,1,1),Tile(0,0,1,1),Tile(1,0,1,0)],
#              [Tile(0,1,1,0),Tile(0,0,1,1),Tile(1,0,0,1)],
#              [Tile(0,1,0,1),Tile(0,0,1,1),Tile(1,0,1,1)],
#              ]


testdungeon = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,1,0,0,0,1],
    [1,0,1,1,0,1,0,1,0,1],
    [1,0,1,0,0,1,0,1,0,1],
    [1,0,1,0,1,1,0,0,0,1],
    [1,0,1,0,1,0,0,0,0,1],
    [1,0,1,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,1,0,1],
    [1,0,0,0,0,0,1,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
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
            if ttype[i] != 1:
                ttype[i] = 0
            else:
                ttype[i] = 1

    if tile == 1:
        for i in range(len(ttype)):
            ttype[i] = 1

    tiletitle = f"{ttype[0]}{ttype[1]}{ttype[2]}{ttype[3]}"
    finaltile = Tile(tiletitle,ttype[0],ttype[1],ttype[2],ttype[3])
    
    return finaltile

dungeon_blueprint = []
def buildDungeon(dungeon_bp):
    global dungeon_blueprint

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


dungeon_current = buildDungeon(testdungeon)
# dungeon_current = dungeon01
# print(dungeon_current)

party_coord = [1,1]
party_facing = 2
check = dungeon_current[party_coord[0]][party_coord[1]]
vision = None
#Facings; N=8, S=2, W=4, E=6

#Game Logic
def update_coord(x,y):
    global party_coord
    global check
    party_coord[0] -= y
    party_coord[1] += x
    check = dungeon_current[party_coord[0]][party_coord[1]]

def update_vision():
    global vision
    if party_facing == 8:
        if check.N == 0:
            front = "Corridor"
        elif check.N == 1:
            front = "Wall"
        elif check.N == 2:
            front = "Door"

        if check.W == 0:
            left = "Corridor"
        elif check.W == 1:
            left = "Wall"
        elif check.W == 2:
            left = "Door"

        if check.E == 0:
            right = "Corridor"
        elif check.E == 1:
            right = "Wall"
        elif check.E == 2:
            right = "Door"

    if party_facing == 2:
        if check.S == 0:
            front = "Corridor"
        elif check.S == 1:
            front = "Wall"
        elif check.S == 2:
            front = "Door"

        if check.E == 0:
            left = "Corridor"
        elif check.E == 1:
            left = "Wall"
        elif check.E == 2:
            left = "Door"

        if check.W == 0:
            right = "Corridor"
        elif check.W == 1:
            right = "Wall"
        elif check.W == 2:
            right = "Door"

    if party_facing == 4:
        if check.W == 0:
            front = "Corridor"
        elif check.W == 1:
            front = "Wall"
        elif check.W == 2:
            front = "Door"

        if check.S == 0:
            left = "Corridor"
        elif check.S == 1:
            left = "Wall"
        elif check.S == 2:
            left = "Door"

        if check.N == 0:
            right = "Corridor"
        elif check.N == 1:
            right = "Wall"
        elif check.N == 2:
            right = "Door"

    if party_facing == 6:
        if check.E == 0:
            front = "Corridor"
        elif check.E == 1:
            front = "Wall"
        elif check.E == 2:
            front = "Door"

        if check.N == 0:
            left = "Corridor"
        elif check.N == 1:
            left = "Wall"
        elif check.N == 2:
            left = "Door"

        if check.S == 0:
            right = "Corridor"
        elif check.S == 1:
            right = "Wall"
        elif check.S == 2:
            right = "Door"

    vision = f"you can see a  {front} in front of you, a  {left} to your left, and a {right} to your right."
    print (vision)

def update_picture():
    if party_facing == 8:
        if check.W == 0 and check.N == 0 and check.E == 0:
            print(t000)
        elif check.W == 1 and check.N == 0 and check.E == 1:
            print(t101)
        elif check.W == 0 and check.N == 1 and check.E == 1:
            print(t011)
        elif check.W == 1 and check.N == 1 and check.E == 0:
            print(t110)
        elif check.W == 0 and check.N == 1 and check.E == 0:
            print(t010)
        elif check.W == 1 and check.N == 1 and check.E == 1:
            print(t111)
        elif check.W == 0 and check.N == 0 and check.E == 1:
            print(t001)
        elif check.W == 1 and check.N == 0 and check.E == 0:
            print(t100)

    elif party_facing == 4:
        if check.S == 0 and check.W == 0 and check.N == 0:
            print(t000)
        elif check.S == 1 and check.W == 0 and check.N == 1:
            print(t101)
        elif check.S == 0 and check.W == 1 and check.N == 1:
            print(t011)
        elif check.S == 1 and check.W == 1 and check.N == 0:
            print(t110)
        elif check.S == 0 and check.W == 1 and check.N == 0:
            print(t010)
        elif check.S == 1 and check.W == 1 and check.N == 1:
            print(t111)
        elif check.S == 1 and check.W == 0 and check.N == 0:
            print(t100)
        elif check.S == 0 and check.W == 0 and check.N == 1:
            print(t001)

    elif party_facing == 2:
        if check.E == 0 and check.S == 0 and check.W == 0:
            print(t000)
        elif check.E == 1 and check.S == 0 and check.W == 1:
            print(t101)
        elif check.E == 0 and check.S == 1 and check.W == 1:
            print(t011)
        elif check.E == 1 and check.S == 1 and check.W == 0:
            print(t110)
        elif check.E == 0 and check.S == 1 and check.W == 0:
            print(t010)
        elif check.E == 1 and check.S == 1 and check.W == 1:
            print(t111)
        elif check.E == 1 and check.S == 0 and check.W == 0:
            print(t100)
        elif check.E == 0 and check.S == 0 and check.W == 1:
            print(t001)
        
    elif party_facing ==6:
        if check.N == 0 and check.E == 0 and check.S == 0:
            print(t000)
        elif check.N == 1 and check.E == 0 and check.S == 1:
            print(t101)
        elif check.N == 0 and check.E == 1 and check.S == 1:
            print(t011)
        elif check.N == 1 and check.E == 1 and check.S == 0:
            print(t110)
        elif check.N == 0 and check.E == 1 and check.S == 0:
            print(t010)
        elif check.N == 1 and check.E == 1 and check.S == 1:
            print(t111)
        elif check.N == 1 and check.E == 0 and check.S == 0:
            print(t100)
        elif check.N == 0 and check.E == 0 and check.S == 1:
            print(t001)

def getMap():

    global dungeon_blueprint
    localmap = [
        [' ','5',' '],
        ['5','0','5'],
        [' ','5',' '],
        ]
    
    NE = dungeon_blueprint[party_coord[0]-1][party_coord[1]+1]
    NW = dungeon_blueprint[party_coord[0]-1][party_coord[1]-1]
    SE = dungeon_blueprint[party_coord[0]+1][party_coord[1]+1]
    SW = dungeon_blueprint[party_coord[0]+1][party_coord[1]-1]

    if party_facing == 8:
        localmap[1][1] = "^"
    elif party_facing == 2:
        localmap[1][1] = "v"
    elif party_facing == 4:
        localmap[1][1] = "<"
    elif party_facing == 6:
        localmap[1][1] = ">"
    
    if NW == 0:
        localmap[0][0] = '0'
    elif NW == 1:
        localmap[0][0] = '1'

    if NE == 0:
        localmap[0][2] = '0'
    elif NE == 1:
        localmap[0][2] = '1'

    if SE == 0:
        localmap[2][2] = '0'
    elif SE == 1:
        localmap[2][2] = '1'

    if SW == 0:
        localmap[2][0] = '0'
    elif SW == 1:
        localmap[2][0] = '1'

    if check.N == 0:
        localmap[0][1] = '0'
    elif check.N == 1:
        localmap[0][1] = '1'

    if check.W == 0:
        localmap[1][0] = '0'
    elif check.W == 1:
        localmap[1][0] = '1'

    if check.E == 0:
        localmap[1][2] = '0'
    elif check.E == 1:
        localmap[1][2] = '1'

    if check.S == 0:
        localmap[2][1] = '0'
    elif check.S == 1:
        localmap[2][1] = '1'

    for n in range(0,len(localmap)):
        # print(f"{localmap[n]}")
        print(' '.join(localmap[n]))

def dungeonMap():
    dungeonmap = ''
    for n in range(0,len(dungeon_current)):
        for y in dungeon_current[n]:
            dungeonmap += f" {y.name}"
        dungeonmap += "\n"
    
    print(dungeonmap)
    pass

#Game Loop
exploring = True
# dungeon_current = buildDungeon(testdungeon)

while exploring == True:
    
    if party_coord == [50,50]:
        
        print ("Congratulations, you reached the end of the dungeon!")
        exploring = False
        print(r"""
                \ _ _ _ /
                 |  _  | 
                 | | | | 
                 | | | |
                /       \
                """)

    if exploring == True:
        getMap()
        # print(party_coord)
        update_picture()
        update_vision()
        
        command = input("""Press 8 to go Forwards, 7 to turn left, and 9 to turn right: """)
    
        os.system('cls')

    if command == "7":
        if party_facing == 8:
            party_facing = 4
        elif party_facing == 4:
            party_facing = 2
        elif party_facing == 2:
            party_facing = 6
        elif party_facing ==6:
            party_facing = 8

    if command == "9":
        if party_facing == 8:
            party_facing = 6
        elif party_facing == 6:
            party_facing = 2
        elif party_facing == 2:
            party_facing = 4
        elif party_facing == 4:
            party_facing = 8

    if command == "8":
        if party_facing == 8:
            if check.N == 0:
                update_coord(0,1)
            elif check.N == 1:
                print ("You bonk against a wall.")
            elif check.N == 2:
                print ("You see a door in front of you.")
        
        elif party_facing == 6:
            if check.E == 0:
                update_coord(1,0)
            elif check.E == 1:
                print ("You bonk against a wall.")
            elif check.E == 2:
                print ("You see a door in front of you.")

        elif party_facing == 2:
            if check.S == 0:
                update_coord(0,-1)
            elif check.S == 1:
                print ("You bonk against a wall.")
            elif check.S == 2:
                print ("You see a door in front of you.")

        elif party_facing == 4:
            if check.W == 0:
                update_coord(-1,0)
            elif check.W == 1:
                print ("You bonk against a wall.")
            elif check.W == 2:
                print ("You see a door in front of you.")

    if command == "map":
        # getMap(party_coord)
        dungeonMap()

        input("Type anything to continue:")


# TEST