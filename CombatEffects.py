## All effects go here!

import math


def applyEffect (caster, effect, char):

    if "enha" in effect:
        effectvalue = (math.sqrt(caster.tec)/10+1) * 5 * caster.slist[effect][0]
    elif "enfe" in effect:
        effectvalue = ((math.sqrt(caster.tec)/10+1) * 5 * caster.slist[effect][0]) * -1
    
    
    char.effects.update({effect: [effectvalue, 3]})

    # ENHA
    if effect == "enhast":
        char.str += effectvalue
        
    elif effect == "enhate":
        char.tec += effectvalue
    
    elif effect == "enhavi":
        char.vit += effectvalue

    elif effect == "enhagi":
        char.agi += effectvalue

    elif effect == "enhalk":
        char.lck += effectvalue

    # ENFE
    elif effect == "enfest":
        char.str += effectvalue
        
    elif effect == "enfete":
        char.tec += effectvalue
    
    elif effect == "enfevi":
        char.vit += effectvalue

    elif effect == "enfegi":
        char.agi += effectvalue

    elif effect == "enfelk":
        char.lck += effectvalue


def tickEffect (char):

    for n in char.effects:
        char.effects[n][1] -= 1
        
        if char.effects[n][1] == 0:
            if n == "enhast":
                char.str -= char.effects[n][0]
            elif n == "enhate":
                char.tec -= char.effects[n][0]
            elif n == "enhavi":
                char.vit -= char.effects[n][0]
            elif n == "enhagi":
                char.agi -= char.effects[n][0]
            elif n == "enhalk":
                char.lck -= char.effects[n][0]

            elif n == "enfest":
                char.str -= char.effects[n][0]
            elif n == "enfete":
                char.tec -= char.effects[n][0]
            elif n == "enfevi":
                char.vit -= char.effects[n][0]
            elif n == "enfegi":
                char.agi -= char.effects[n][0]
            elif n == "enfelk":
                char.lck -= char.effects[n][0]
            
            
            char.effects.pop(n)