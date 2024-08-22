import random

def simulate(attackerarmies, defenderarmies):
    randomifier = random.randint(0,4)
    if randomifier == 0 or randomifier == 1:
        return (attackerarmies-1, defenderarmies-1)
    elif randomifier == 2 or randomifier == 3:
        return (attackerarmies, defenderarmies-1)
    elif randomifier == 4:
        return (attackerarmies-1, defenderarmies)