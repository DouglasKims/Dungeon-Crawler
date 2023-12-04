
# PROJECT OVERALL
    # Create a file just for characters and classes

# PERKS
    # Every 5/10(?) levels, characters get access to new spell level/type
    
# DUNGEON CRAWLER PART
    # Try to implement a random dungeon generator?

    # Field Bosses (DONE)
        # To do this, the code needs a "fieldmap" that contains the whole dungeon, but shows only where the group is at, at a 3x3/5x5 grid around the party. (doable, but requires big rewrite, however, allows for Field bosses)

    # Implement Doors and Objects (chests/treasure) (DONE)
    # Implement Rest Area
    # Implement Merchant 


# IMPLEMENT CITY (& QUESTS?)
    # City

# COMBAT & SKILLS
    # Rename Skills
    # Use items in combat
    # Escape combat
    # create buff, debuff skills

    # Enemy Generator? (DONE)
    #  Fix formulas (DONE)

# CLASS SKILLS
    # KNIGHT
        # SKILLS
            # CHARGE attack 1 opp up to 3 times (lvl 1/10)
            # CLEAVE attack random opps up to 5 times (lvl 1/10)
            # PROTECT reduce damage to all by 10%/lvl (lvl 1/10)
        # PERKS
            # STR boost for one lv1 / party lv3 for lvl turns (lvl 1/5)
            # VIT boost for one lv1 / party lv3 for lvl turns (lvl 1/5)
            # Chance to resist death 10%/lvl (lvl 1/5)

    # THAUMATURGE
        # SKILLS # FP cost reduced / lvl
            # ELEMENTAL damage weak lv1 / multi lvl 3 / med lvl 5 / heavy lvl 7 (lvl 1/10)
            # HEALING weak lvl 1 / multi lvl 2 / med lvl 3 / heavy lvl 4 (lvl 1/10)
            # REVIVE weak lvl 1 / multi lvl 3 / med lvl 5 / full lvl 7 (lvl 1/10)
        # PERKS
            # Restore HP at end of combat lvl 1 / per turn lvl 3 / per step lvl 5 (lvl 1/5)
            # Healing skills restore TP as well (lvl 1/5)
            # Life drain attack

    # ARCANIST
        # SKILLS # FP cost reduced / lvl
            # ELEMENTAL damage weak lvl 1 / multi lvl 2 / med lvl 3 / heavy lvl 4 (lvl 1/10)
            # BOOST TEC %/lvl (lvl 1/10)
            # BOOST LCK (lvl 1/10)
        # PERKS
            # Restore FP per enemy you kill lvl1 / at end of combat lvl 3 / per turn lvl 5 (lvl 1/5)
            # Reflect damage to enemies (lvl 1/5)
            # New Element Type (lvl 1/5)

    # SCOUT
        # SKILLS
            # SNEAK hit one opp with increased crit chance (lvl 1/10)
            # DECOY Create a false target with it's own HP pool (lvl 1/10)
            # HUNT deal more damage to a creature whose HP is higher (lvl 1/10)
        # PERKS
            # ANALYZE enemy weaknesses and resistances, HP and STATS (lvl 1/5)
            # COUNTER deal back damage to attacker (lvl 1/5)
            # RIPOSTE freely attack an enemy that misses you (lvl 1/5)

    # HERALD
        # SKILLS
            # ELEMENTAL damage weak lvl 1 / multi lvl 4 / med lvl 8 (lvl 1/10)
            # HEALING weak lvl 1 / multi lvl 3 / med lvl 5 / hvy lvl 7 (lvl 1/10)
            # BOOST STR lvl 1/ MSTR lvl 2 / VIT lvl 3 / MVIT lvl 4 / TEC lvl 5 / MTEC lvl 6 / AGI lvl 7 / MAGI lvl 8 / LCK lvl 9 / MLCK lvl 10 (lvl 1/10)
        # PERKS
            # Boosting allies restores HP (lvl 1/5)
            # Killing enemies restores HP (lvl 1/5)
            # Healing allies grants a random boon (lvl 1/5)

    # QUARTERMASTER
        # SKILLS
            # MONEY SHOOT Attack with money, increasing STR and LCK the more money is spent (lvl 1/10)
            # COATING grants elemental resistance for a few turns / for party (lvl 1/10)
            # APPRAISE increases EXP gain / high TP cost (lvl 1/10)
        # PERKS
            # Increase loot drop rate (lvl 1/5)
            # Freely produces a consumable after X amount of steps (lvl 1/5)
            # Chance of not consuming items (lvl 1/5)




# DAMAGES AND ELEMENTS names, types?
    # Almighty        buff / debuff / damage / Heal
    # yabarag         atk + / atk - / thunder / rage-
    # haka pf'hagan   haste / slow / decay / regen
    # igglebeth       resist death + / kill / toxic / revive
    # irgh d'ebram    mdef + / mdef -/ ice / poison-
    # famphegor       reflect / sleep / air / confuse -
    # gaaphadur       pdef + / pdef - / earth / condition -
    # pasperon        lck + / lck- / fire / heal
    # khosme          - / - / chaos / 

    # Grun > Several targets
    # Lag > weak damage / negative (weak / lag)
    # Comas > medium damage / negative (capable / comasach)
    # Asmatha > heavy damage / negative (biggest/motha)
    # Tin > weak heal / positive (ill / tinn)
    # Cruai > medium heal / positive (tough / cruaidh)
    # Fallain > heavy heal / positive (fallain / healthy)
    # Leas > buff (improve / leasaich)
    # Mios > debuff (worse / nas miosa)

    # fire > Grun/Pas/mor // /Pas/matha
    # water > Grun/Irg/mor // Irg/matha
    # earth > Grun/Gaa/mor // Gaa/matha
    # air > Grun/Fam/mor // Fam/matha

    Fire    //  Firo / mor / matha
    Ice     //  Gelo
    Earth   //  Tera
    Air     //  Gale
    Thunder //  Volt
    Creation//  Cura
    Toxic   //  Veno
    Chaos   //  Nuke

    Revive  //  Revita / mor / matha

    Weak damage spell = 4 TP
    weak damage spell group (grun) = 10 TP
    medium damage spell (mor) =  8 TP
    medium damage spell group (grun/mor) = 16 TP
    heavy damage spell (matha) = 12 TP
    heavy damage spell group (grun/matha) = 22 TP