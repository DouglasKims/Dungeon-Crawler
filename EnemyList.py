# ENEMY LIST

class Enemy:
    def __init__(self,name,level,maxhp,hp,tp,str,dmg,tec,vit,agi,lck,defending,weak,resist,exp,money,init, effects):
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
        self.resist = resist
        self.exp = exp
        self.money = money
        self.init = init
        self.effects = effects
#          0    1       2       3       4       5       6       7       8
elem = ["phys","fire","wind","earth","ice","thunder","toxic","chaos","death"]
# ENEMY TYPES
    # Malla // Basic physical attacks (Weak: Fire or Ice or Wind or Earth or None/ Resist: Phys)
    # Sgeu // High SPD baits misses on phys attacks (Weak: Phys AND Ice or Earth/ Resist: None)
    # Diogh // Always picks the same target for Phys attacks (Weak: Fire or Ice or Wind or Earth or Thunder AND Toxic / Resist: None)
    # Colt // random phys or elemental attacks (Weak: Two of Fire or Ice or Wind or Earth or Thunder or Toxic ; Resist: None)
    # Adhbah // Debufs and spell attacks (Weak: None / Resist: One element)
    # Grain // strong spell attacks or AOE spell attacks (Weak: None / Resist: Two elements)

    # Laidir // Bosses

    # Level 1 // Puny, Weak, Cowardly
    # Level 2 // Malicious, Insidious, Cruel
    # Level 3 // Hateful, Spiteful, Wrathful
    # Level 4 // Angry, Merciless, Viscerous
    # Level 5 // Cursed, Divisive, Unpleasant

# FIRST FLOOR ENEMIES


en_laid1 = Enemy(name = "Puny Làidir",
    level = 8, maxhp = 450, hp = 450, tp = 30, str = 20, dmg = 2, tec = 15, vit = 10, agi = 5, lck = 5,
    defending = False, weak = [],resist = [], exp = 5, money = 100, init = 0, effects = {})


enemies_1 = []

enemies_bosses = [en_laid1]