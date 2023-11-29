# ENEMY LIST

class Enemy:
    def __init__(self,name,level,maxhp,hp,tp,str,dmg,tec,vit,agi,lck,defending,weak,exp,money,init):
        self.name = name
        self.level = level
        self.maxhp = maxhp
        self.hp = hp
        self.tp = tp
        self.str = str
        self.dmg = dmg
        self.tec = tec
        self.vit = vit
        self.agi = agi
        self.lck = lck
        self.defending = defending
        self.weak = weak
        self.exp = exp
        self.money = money
        self.init = init
#          0    1       2       3       4       5       6       7       8       9
elem = ["phys","fire","wind","earth","ice","thunder","toxic","decay","chaos","death"]
# ENEMY TYPES
    # Malla // Basic physical attacks
    # Sgeu // High SPD baits misses on phys attacks
    # Diogh // Always picks the same target for Phys attacks
    # Colt // random phys or elemental attacks
    # Adhbah // Debufs and spell attacks
    # Grain // strong spell attacks or AOE spell attacks

    # Laidir // Bosses

    # Level 1 // Puny, Weak, Cowardly
    # Level 2 // Malicious, Insidious, Cruel
    # Level 3 // Hateful, Spiteful, Wrathful
    # Level 4 // Angry, Merciless, Viscerous
    # Level 5 // Cursed, Divisive, Unpleasant

# FIRST FLOOR ENEMIES
en_mal1 = Enemy(
    name = "Puny Malla",
    level = 1,
    maxhp = 40,
    hp = 40,
    tp = 10,
    str = 5,
    dmg = 1,
    tec = 2,
    vit = 3,
    agi = 3,
    lck = 3,
    defending = False,
    weak = [],
    exp = 5,
    money = 5,
    init = 0)
en_sgeu1 = Enemy(
    name = "Weak Sgeu",
    level = 1,
    maxhp = 30,
    hp = 30,
    tp = 10,
    str = 4,
    dmg = 1,
    tec = 2,
    vit = 4,
    agi = 8,
    lck = 4,
    defending = False,
    weak = [],
    exp = 5,
    money = 5,
    init = 0)
en_dio2 = Enemy(
    name = "Cowardly Diogh",
    level = 2,
    maxhp = 60,
    hp = 60,
    tp = 20,
    str = 8,
    dmg = 1,
    tec = 5,
    vit = 7,
    agi = 4,
    lck = 4,
    defending = False,
    weak = [],
    exp = 10,
    money = 10,
    init = 0)
en_colt2 = Enemy(
    name = "Malicious Colt",
    level = 2,
    maxhp = 50,
    hp = 50,
    tp = 20,
    str = 7,
    dmg = 1,
    tec = 5,
    vit = 7,
    agi = 4,
    lck = 4,
    defending = False,
    weak = [],
    exp = 10,
    money = 10,
    init = 0)
en_adhbah1 = Enemy(
    name = "Insidious Adhbah",
    level = 1,
    maxhp = 40,
    hp = 40,
    tp = 30,
    str = 3,
    dmg = 1,
    tec = 6,
    vit = 3,
    agi = 3,
    lck = 3,
    defending = False,
    weak = [],
    exp = 5,
    money = 5,
    init = 0)
en_adhbah2 = Enemy(
    name = "Hateful Adhbah",
    level = 2,
    maxhp = 45,
    hp = 45,
    tp = 40,
    str = 5,
    dmg = 1,
    tec = 11,
    vit = 7,
    agi = 5,
    lck = 5,
    defending = False,
    weak = [],
    exp = 10,
    money = 10,
    init = 0)
en_grain1 = Enemy(
    name = "Viscerous Grain",
    level = 1,
    maxhp = 30,
    hp = 30,
    tp = 20,
    str = 2,
    dmg = 1,
    tec = 8,
    vit = 2,
    agi = 4,
    lck = 3,
    defending = False,
    weak = [],
    exp = 5,
    money = 5,
    init = 0)

# enemy2 = Enemy("Malignant Spirit",2,40,40,5,1,0,5,0,False,[elem[0],elem[2]],10,10,0)
# enemy3 = Enemy("Despicable Shade",3,30,30,4,1,2,6,0,False,[elem[1],elem[3]],15,20,0)
# enemy4 = Enemy("Troublesome Ghost",1,80,80,5,1,3,2,0,False,[elem[1],elem[2],elem[3],elem[4],elem[5],elem[6]],5,5,0)

en_laid1 = Enemy(name = "Puny Làidir",
    level = 1, maxhp = 200, hp = 200, tp = 30, str = 20, dmg = 2, tec = 15, vit = 10, agi = 5, lck = 5,
    defending = False, weak = [], exp = 5, money = 100, init = 0)


enemies_1 = [en_mal1,en_sgeu1,en_dio2,en_colt2,en_adhbah1,en_adhbah2,en_grain1]

enemies_bosses = [en_laid1]