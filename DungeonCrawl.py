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
t101 = """
 \ _ _ _ /
  |     | 
  |     | 
  |     |
 /       \\
"""
t011 = """
 _ _ _ _ /
  |     | 
  |     | 
 _|_ _ _|
         \\
"""

t110 = """
 \ _ _ _ _
  |     | 
  |     | 
  |_ _ _|_
 /        
"""
t010 = """
 _ _ _ _ _
  |     | 
  |     | 
 _|_ _ _|_
          
"""
t000 = """
 _ _ _ _ _
  |     | 
  |     | 
 _|     |_
          
"""
t111 = """
 \ _ _ _ /
  |     | 
  |     | 
  |_ _ _|
 /       \\
"""
t001 = """
 _ _ _ _ /
  |     | 
  |     | 
 _|     |
         \\
"""
t100 = """
 \ _ _ _ _
  |     | 
  |     | 
  |     |_
 /       
"""



# Subtypes Open(0),Wall(1),Door(2)
class Tile:
    def __init__(self,N,S,W,E):
        self.N = N
        self.S = S
        self.E = E
        self.W = W

dungeon01 = [[Tile(0,1,1,1),Tile(0,0,1,1),Tile(1,0,1,0)],

             [Tile(0,1,1,0),Tile(0,0,1,1),Tile(1,0,0,1)],

             [Tile(0,1,0,1),Tile(0,0,1,1),Tile(1,0,1,1)],
             ]

party_coord = [0,0]
party_facing = 8
check = dungeon01[party_coord[0]][party_coord[1]]
vision = None
#Facings; N=8, S=2, W=4, E=6

#Game Logic
def update_coord(x,y):
    global party_coord
    global check
    party_coord[0] += x
    party_coord[1] += y
    check = dungeon01[party_coord[0]][party_coord[1]]

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

    
#Game Loop
exploring = True
while exploring == True:
    
    if party_coord == [2,2]:
        
        print ("Congratulations, you reached the end of the dungeon!")
        exploring = False
        print("""
                \ _ _ _ /
                 |  _  | 
                 | | | | 
                 | | | |
                /       \\
                """)

    if exploring == True:
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

