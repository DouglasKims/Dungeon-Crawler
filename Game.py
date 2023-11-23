import CombatSystem
import EquipmentSystem
from math import e
import os
import time
import random
import copy


gamerunning = True

while gamerunning == True:
    
    os.system("cls")
    gamecommand = input(f"What do you want to do?\n (C)ombat\n (E)quipment\n (D)ungeon\n")

    if gamecommand.lower() == "c":

        CombatSystem.runCombat()

        # runCombat() Func
            # CombatSystem.randomenemies()
            # CombatSystem.rollinitiative()
            # initnames = ", ".join(str(n.name) for n in CombatSystem.initiative)
            # print (f"Turn order: {initnames}")

            # rounds = 0
            # testing_combat = True
            # while testing_combat:

            #     os.system('cls')

            #     if not CombatSystem.opposition:
            #         testing = False
            #         print(f"You won the combat in {rounds} rounds!")
            #         break

            #     rounds += 1
            #     print (f"Round {rounds}")
            #     print ("") #spacer
            #     print ("Party:") #spacer
            #     for n in CombatSystem.party:
            #         print (f"({CombatSystem.party.index(n)}) {n.name}'s HP: {n.hp}/{n.maxhp} /// FP: {n.fp}/{n.maxfp}")
            #     print ("") #spacer
            #     print ("Opposition") #spacer
            #     for n in CombatSystem.opposition:
            #         print (f"({CombatSystem.opposition.index(n)}) {n.name}'s HP is {round(n.hp/n.maxhp*100)}%")
            #     print ("") #spacer

            #     initnames = ", ".join(str(n.name) for n in CombatSystem.initiative)
            #     print (f"Turn order: {initnames}")
                
            #     print ("") #spacer

            #     for n in CombatSystem.initiative:
            #         if n not in CombatSystem.party and n.hp <= 0:
            #             pass
            #         else:
            #             print(f"It's {n.name}'s turn!")
            #         if n in CombatSystem.party and n.hp <= 0:
            #             print (f"But they're down.")
            #             print ("")

            #         if n in CombatSystem.opposition and n.hp > 0:
            #             enemytarget = None
            #             while enemytarget == None or enemytarget.hp == 0:
            #                 enemytarget = random.choice(CombatSystem.party)
            #             CombatSystem.attackfunc(n,enemytarget)

            #             #game over function
            #             if CombatSystem.gameover(CombatSystem.party):
            #                 print ("")
            #                 print ("All heroes have been defeated.")
            #                 break

            #             print ("")
            #             time.sleep(0.4)
                    
            #         elif n in CombatSystem.party:
            #             n.acted = False
            #             n.defending = False
            #             if not CombatSystem.opposition:
            #                 pass
            #             elif n.hp <= 0:
            #                 pass
            #             else:
            #                 while n.acted == False:
            #                     CombatSystem.command(n)

            #                 print ("")
            #                 time.sleep(0.4)

            #     if CombatSystem.gameover(CombatSystem.party):
            #         print ("")
            #         print ("Game Over.")
            #         break

            #     CombatSystem.endofturncleanup()

            #     input("Type anything to continue: ")

    elif gamecommand.lower() == "e":

        EquipmentSystem.runEquipment()


    # Create PHYS skills for non-casters (buffs, defense, physical attacks)
        # Multi-hit variant for all enemies
        # Medium/Heavy damage variants
        # High crit rate attack

    # Create equipment system
        # equipping and unequipping equipment (shouldn't be done in combat)
        # equip. should increase heroes' ATK, DEF, (maybe change weak/resist)

    # Create Perks system
        # defeating enemies grant EXP, each EXP*perks+1 reached gives a new perk.
        # Perks can increase > base HP, FP, SPD, LCK, TEC
        # SPD/LCK/TEC can't be higher than 15
        # HP increases are based on class / 10% of class' max
        # FP increases are based on class / 10% of class' max
        # Every 10(?) perks, characters get access to new spell level/type


    # mu/fire > mu/fireza > mu/firezaon
    # mul/ice > mul/iceza > mul/icezaon
    # mul/air > mul/airza > mul/airzaon
    # mu/rock > mu/rockza > mu/rockzaon
    # mu/zap > mu/zapza > mu/zapzaon
    # mu/tox > mu/toxza > mu/toxzaon

    # fire / fire-sta / fire-sta-za
    # fire-mor (big) / fire-mortha (biggest)

    # cure / curemor / curemortha
    # revive / revivemor

    # haste / slow
    # shield / barrier

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